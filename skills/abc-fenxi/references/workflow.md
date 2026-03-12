# abc-fenxi 完整执行步骤（Handoff 文档）

> **目标读者**：负责实现 abc-fenxi skill 的开发者
> **版本**：v1.0（2026-03-11）
> **前提**：请先阅读 skill.md 了解整体架构

---

## 0. 用户调用入口

用户通过以下方式触发：

```
# 方式1：通过 chai-shu 主入口选择选项7
请帮我拆书。
源项目目录：{ROOT}/Factory/拆书/（书名）/
任务：ABC分析

# 方式2：直接触发
请对这个拆书项目做ABC分析。
源项目目录：{ROOT}/Factory/拆书/（书名）/
```

---

## 1. 阶段0：前置检查（主进程执行）

### 1.1 依赖验证

```python
# 伪代码：主进程执行的检查逻辑

项目目录 = 用户提供的路径
概括目录 = 项目目录 + "/概括/"
全书概括 = 项目目录 + "/全书概括.md"
名词表 = 项目目录 + "/人物和设定/名词表.md"
输出目录 = 项目目录 + "/ABC分析/"

# 检查1：概括目录是否存在
if 概括目录不存在:
    → 报错："未找到概括目录，请先执行分章节概括（chai-shu 选项3）"
    → 终止

# 检查2：计算概括文件数
概括文件列表 = glob("{概括目录}/组*_概括.md")  # 匹配所有概括组文件
总章节数 = 从文件列表中解析章节范围

if 总章节数 == 0:
    → 报错："概括目录为空"
    → 终止

# 检查3：增量更新判断
进度文件 = 输出目录 + "/_progress.json"
if 进度文件存在:
    → 读取已处理章节列表
    → 计算待处理章节（仅处理新增）
else:
    → 全量分析
    → 创建输出目录
```

### 1.2 进度文件格式

```json
{
  "book": "书名",
  "total_chapters": 50,
  "analyzed_chapters": ["001", "002", "003"],
  "last_updated": "2026-03-11",
  "batches_completed": ["batch_1_ch001-005", "batch_2_ch006-010"]
}
```

### 1.3 向用户报告

完成检查后，主进程向用户确认：

```
✅ 前置检查通过
  - 找到概括文件：X 个（覆盖 Y 章）
  - ABC分析目录：已初始化
  - 增量模式：全量 / 仅处理第 Z-N 章（增量时显示）

开始ABC分析，分 M 批并行处理，预计 N 分钟完成。
```

---

## 2. 阶段1：批量并行分析（主进程调度 + 批次 sub-agent）

### 2.1 分批参数计算

```python
章节列表 = [待分析的章节序号列表]
批次大小 = 5
并行上限 = 3

批次列表 = [
    章节列表[i:i+5]
    for i in range(0, len(章节列表), 5)
]

# 例：50章 → 10个批次
# 执行方式：每轮最多3个批次并行
# 第1轮：批次1（ch001-005）、批次2（ch006-010）、批次3（ch011-015）
# 第2轮：批次4（ch016-020）、批次5（ch021-025）、批次6（ch026-030）
# ...
```

### 2.2 批次 sub-agent 调用规范

**主进程启动 sub-agent 的 prompt 格式**（参见 references/sub-agent-prompt.md 获取完整提示词）：

```
你是一个ABC爽点分析执行者。

任务：分析以下章节的ABC结构
批次ID：batch_N
待分析章节：[章节序号列表]
概括文件目录：{概括目录路径}
输出目录：{输出目录路径}
名词表路径：{名词表路径}
ABC定义文档路径：{skill目录}/references/abc-definition.md

执行步骤：
1. 读取 abc-definition.md（识别规则）
2. 读取名词表（了解人物名称）
3. 对每个章节概括文件逐章分析：
   a. 识别章节中的 ABC 循环（最多3个）
   b. 生成快捷列表（quick_list）：按时间顺序提取5-15个情节点，标注ABC标签，识别过渡点（B→A'⟳）
   c. 完成分析后执行自审（见 abc-definition.md 结尾的自审清单，含quick_list和过渡点检查）
   d. 输出 abc-ch{XXX}.yaml 到输出目录
4. 所有章节完成后，回复：
   "批次N完成：已生成 abc-ch{XXX}.yaml, abc-ch{YYY}.yaml, ..."
```

### 2.3 主进程等待与进度追踪

```python
# 主进程的调度逻辑（伪代码）

for 每轮 in 批次列表按三个分组:
    并行启动本轮的最多3个sub-agent
    等待本轮所有sub-agent完成

    # 验证：检查每个预期输出文件是否存在
    for 批次 in 本轮批次:
        for 章节 in 批次:
            if abc-ch{章节}.yaml 不存在:
                → 记录失败
                → 重试该批次（最多1次）

    # 更新进度文件
    更新 _progress.json

    # 向用户报告进度
    print(f"进度：已完成 {已完成章节数}/{总章节数} 章")
```

### 2.4 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| sub-agent 未返回完成确认 | 等待30秒后检查输出文件是否存在 |
| 输出文件不存在 | 重启该批次 sub-agent，最多重试1次 |
| 重试仍失败 | 跳过该批次，记录到 _progress.json 的 `failed_batches` 字段 |
| 所有批次完成但有失败 | 向用户报告失败批次，询问是否重试 |

---

## 3. 阶段2：全书汇总（汇总 sub-agent）

### 3.1 触发条件

所有批次（包括重试）完成后，主进程启动汇总 sub-agent。

### 3.2 汇总 sub-agent 输入

```
任务：生成全书 ABC 汇总分析

输入文件目录：{输出目录}（包含所有 abc-ch*.yaml）
全书概括路径：{全书概括.md}
名词表路径：{名词表.md}
输出文件1：{输出目录}/abc-summary.yaml
输出文件2：{输出目录}/abc-heatmap.md
输出文件3：{输出目录}/abc-quick-list.md

执行步骤：
1. 读取所有 abc-ch*.yaml 文件
2. 计算全书指标（见下方字段说明）
3. 识别爽点峰值章（structure_quality≥4.5的章节）
4. 识别问题章（structure_quality≤2.0，或B完整度不合格）
5. 分析节奏（连续低密度区间）
5.5. 生成快捷列表汇总（abc-quick-list.md）：遍历所有章节YAML的quick_list字段，按章节顺序拼接为Markdown；统计全书过渡点（B→A'⟳）总数；旧版YAML无quick_list字段时标注"待补充"
6. 输出 abc-summary.yaml
7. 输出 abc-heatmap.md（可视化）
8. 输出 abc-quick-list.md（快捷列表汇总）
```

### 3.3 abc-summary.yaml 字段规范

```yaml
book_title: "（书名）"
analyzed_at: "（日期）"
total_chapters: N
analyzed_chapters: N

overall_metrics:
  high_density_count: N    # structure_quality≥3.5 的章节数
  medium_density_count: N
  low_density_count: N
  abc_density_ratio: "XX%"   # 高密度占比
  avg_structure_quality: X.X  # 平均综合评分
  b_reaction_pass_rate: "XX%"  # B完整度合格率

top_chapters:              # 最多列5章
  - chapter_id: "XXX"
    title: "（章节标题）"
    reason: "（爽点突出原因）"
    structure_quality: X.X

weak_chapters:             # 最多列5章
  - chapter_id: "XXX"
    title: "（章节标题）"
    reason: "（问题描述）"
    structure_quality: X.X
    suggestion: "（具体改进建议）"

pacing_analysis:
  rhythm_pattern: "（整体节奏描述，如每5-8章出现峰值）"
  dry_spells:              # 连续低密度区间（3+章）
    - chapters: "ch018-ch022"
      suggestion: "（改善建议）"

b_reaction_analysis:
  avg_reaction_ratio: X.X  # 全书平均反应篇幅比
  most_common_issue: "（最常见的B问题）"
  pass_count: N
  fail_count: N

c_hook_analysis:
  chapters_with_hook: N
  chapters_without_hook: N
  most_effective_c_type: "（最常用的C类型）"
```

### 3.4 abc-heatmap.md 格式

```markdown
# ABC爽点密度热力图 — 《书名》

## 全书爽点分布

| 章节 | A | B | C | 综合 | 备注 |
|------|---|---|---|------|------|
| 第1章 | ★★★★☆ | ★★★★★ | ★★★☆☆ | 4.5 | 🔥峰值 |
| 第2章 | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | 3.0 | |
| ...  | ... | ... | ... | ... | |

## 节奏概览

（用文字描述爽点分布规律、峰值位置、低谷区间）

## 问题章节
（列出需要关注的章节和改进建议）
```

---

## 4. 主进程最终报告

全部完成后，主进程向用户输出：

```
✅ ABC分析完成

📊 全书概览：
  - 总章节：N 章
  - 高密度章节：N 章（XX%）
  - B反应合格率：XX%
  - 平均综合评分：X.X / 5.0

🔥 爽点峰值：第X章、第Y章、第Z章
⚠️ 需要关注：第A章、第B章（B反应不足）

📁 输出文件：
  - {书名}/ABC分析/abc-ch001.yaml ... abc-ch0XX.yaml
  - {书名}/ABC分析/abc-summary.yaml
  - {书名}/ABC分析/abc-heatmap.md
  - {书名}/ABC分析/abc-quick-list.md
```

---

## 5. 与 chai-shu 主入口的集成

在 chai-shu/skill.md 中需要做的修改：

```markdown
## 功能菜单

📚 船板拆书（原版）

1. 自动化拆书  → 顺序执行 2→3→4→5→6
2. 拆分扫描    → 扫描结构 + 执行拆分
3. 分章节概括  → 逐章/逐组生成概括（依赖2）
4. 全书概括    → 生成全书理解（依赖3）
5. 人物概括    → 人物关系概要（依赖3）
6. 事件概括    → 事件线追踪（依赖3）
7. ABC分析     → 爽点循环结构分析（依赖3）  ← 新增
```

子 skill 路由表新增一行：
```markdown
| 7 | `abc-fenxi` |
```

---

## 6. 测试计划

### 6.1 测试书籍推荐

```
候选1（首选）：魔法学院的闪现天才
  路径：Factory/拆书/魔法学院的闪现天才[精校版]/
  原因：已有拆分，需确认是否完成分章节概括

候选2：另选一本不同题材爽文（都市/修仙/异能等）
  用于验证 ABC 识别规则的跨题材适配性
```

### 6.2 验收标准

| 测试项 | 通过标准 |
|--------|---------|
| 单章分析准确度 | B反应评分与人工判断误差≤1星 |
| 反应篇幅比计算 | 不合格章节能被正确识别和标注 |
| 批次并行稳定性 | 3批并行时无遗漏，无冲突 |
| 增量更新 | 新增章节后只处理新增部分 |
| 汇总准确度 | 峰值章/问题章判断符合人工预期 |

---

## 7. 开发注意事项

1. **abc-definition.md 必须在 skill 目录内**：sub-agent 需要在运行时读取。将 `Factory/ABC拆书法集成/abc-definition.md` 的内容复制到 `references/abc-definition.md`。

2. **并行上限控制**：ClaudeCode Agent 工具并行调用无硬性限制，但超过5批并行时上下文消耗可能影响主进程稳定性。建议保持3批并行上限。

3. **自审是核心质量控制**：sub-agent 不只是输出结果，必须执行自审（重读 abc-definition，验证自己的评分）。这是保证 B 评分准确的关键。

4. **章节序号格式**：文件名中使用3位补零格式（001, 002, ... 100），确保文件系统排序正确。

5. **概括文件路径**：现有概括文件命名为 `组N_第X-Y章_概括.md`，sub-agent 需要正确解析这个格式并知道哪个组文件包含哪些章节。
