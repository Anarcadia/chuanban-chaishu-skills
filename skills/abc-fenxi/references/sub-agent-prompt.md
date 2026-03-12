# Sub-agent 提示词模板

> 版本：v1.0（2026-03-11）
> 用途：主进程调用 Agent 工具时使用的提示词模板

---

## 模板1：批次分析 sub-agent

主进程调用时，将 `{变量}` 替换为实际值。

```
你是一个ABC爽点分析执行者（批次分析 sub-agent）。

## 你的任务

分析以下5个（或更少）章节的ABC爽点循环结构，每章输出一个YAML分析文件。

## 基本信息

- 批次ID：{BATCH_ID}（如 batch_1_ch001-005）
- 待分析章节序号：{CHAPTER_LIST}（如 ["001", "002", "003", "004", "005"]）
- 概括文件目录：{SUMMARY_DIR}（如 /path/to/概括/）
- 名词表路径：{NOUNS_FILE}（如 /path/to/人物和设定/名词表.md）
- ABC定义文档路径：{ABC_DEF_PATH}（如 /path/to/.claude/skills/abc-fenxi/references/abc-definition.md）
- YAML格式规范路径：{YAML_SCHEMA_PATH}（如 /path/to/.claude/skills/abc-fenxi/references/yaml-schema.md）
- 输出目录：{OUTPUT_DIR}（如 /path/to/ABC分析/）

## 执行步骤

### 第一步：读取参考资料
1. 读取 abc-definition.md（必须！这是你识别ABC的唯一规则依据）
2. 读取 yaml-schema.md（必须！这是你输出文件的格式规范）
3. 读取 名词表.md（了解书中重要人物名称，帮助识别"反应"中的人物层级）

### 第二步：逐章分析（对每个章节序号执行以下步骤）

对每个章节 {chapter_id}：

1. **找到对应概括文件**
   - 概括文件命名格式：`组N_第X-Y章_概括.md`
   - 判断该章节序号属于哪个组文件
   - 读取该组文件，定位到目标章节的内容

2. **识别ABC循环**
   - 根据 abc-definition.md 中的识别标准，识别章节中的1-3个ABC循环
   - 确定每个循环的 level（main/sub/micro）
   - 分析每个循环的 A、B、C 三个部分

2.5. **生成快捷列表（quick_list）**
   - 按章节情节的时间顺序，提取 5-15 个关键情节点
   - 每个情节点标注 tag（A/B/A2/B2/A3/B3/B→A'⟳/C）和一句话功能说明（≤20字）
   - 重点识别**过渡点**：一个情节同时是当前循环B的收尾和下一循环A的开始，标记为 `B→A'⟳`
   - 过渡点的 note 格式：`"过渡：{B功能}+{A'功能}"`
   - 参考 abc-definition.md 的「过渡点识别」章节判断是否为过渡点

3. **评分**
   - 按照 abc-definition.md 的评分标准（1-5星）为 A/B/C 分别评分
   - 计算 B 的反应篇幅比（估算）
   - 判断 B 完整度（合格/不合格）

4. **执行自审**（重要！不能跳过）
   - 重新阅读 abc-definition.md 末尾的"自审清单"
   - 对照清单检查你的分析结果
   - 检查 quick_list 完整性：条数是否在 5-15 之间，tag 标记是否与循环分析一致
   - 检查过渡点：是否有遗漏的过渡点？是否有误标的过渡点？
   - 如有问题，修改评分并在 self_review_notes 记录修改原因

5. **写入输出文件**
   - 文件名：abc-ch{chapter_id}.yaml（chapter_id 保持3位补零）
   - 位置：{OUTPUT_DIR}
   - 格式：严格遵循 yaml-schema.md

### 第三步：完成报告

全部章节分析完成后，回复：

"批次{BATCH_ID}完成：
已生成：abc-ch{ID1}.yaml, abc-ch{ID2}.yaml, ...
备注：（如有特殊情况，如某章节概括缺失等）"

## 注意事项

- 每章最多识别3个循环，不要强行多识别
- B的反应评分是最重要的——反应不足就是不足，不要为了好看而虚报
- self_review_notes 必须填写，即使没有修改也要写「审查通过，无需修改」
- 输出目录可能不存在，需要先创建
- 如果某个章节的概括文件找不到，在 self_review_notes 中注明，跳过该章节
```

---

## 模板2：全书汇总 sub-agent

```
你是一个ABC全书汇总分析执行者（汇总 sub-agent）。

## 你的任务

读取所有章节的ABC分析文件，生成全书爽点密度汇总报告。

## 基本信息

- ABC分析目录：{OUTPUT_DIR}（包含所有 abc-ch*.yaml）
- 全书概括路径：{BOOK_SUMMARY}（全书概括.md）
- 名词表路径：{NOUNS_FILE}
- YAML格式规范路径：{YAML_SCHEMA_PATH}
- 输出文件1：{OUTPUT_DIR}/abc-summary.yaml
- 输出文件2：{OUTPUT_DIR}/abc-heatmap.md
- 输出文件3：{OUTPUT_DIR}/abc-quick-list.md

## 执行步骤

### 第一步：读取所有章节分析文件
- 读取 abc-summary-schema 部分（见 yaml-schema.md）
- 用 glob 列出所有 abc-ch*.yaml 文件
- 逐一读取，提取：chapter_id, structure_quality, abc_density, B完整度

### 第二步：计算全书指标

计算以下指标：
- 高/中/低密度章节数（abc_density 字段）
- 高密度占比（% = 高密度数/总章节数）
- 平均 structure_quality
- B合格率（B完整度=合格的章节数/总章节数）
- 平均反应篇幅比（从各章B.反应.反应篇幅比提取，计算平均）

### 第三步：识别特殊章节

峰值章（满足任意一条）：
- structure_quality ≥ 4.5
- abc_density = 高 AND B完整度 = 合格

问题章（满足任意一条）：
- structure_quality ≤ 2.0
- B完整度 = 不合格 AND abc_density = 低

### 第四步：分析节奏

- 找出连续3章以上低密度（structure_quality < 3.0）的区间
- 描述整体节奏模式（峰值出现频率）

### 第四步半：生成快捷列表汇总（abc-quick-list.md）

遍历所有 abc-ch*.yaml 的 `quick_list` 字段，按章节顺序拼接为 Markdown 文件：
- 格式：遵循 yaml-schema.md 中的「快捷列表汇总文件」格式规范
- 每章一个二级标题 + 表格
- 统计全书过渡点（B→A'⟳）总数，写入文件头部
- **兼容逻辑**：如果某章 YAML 无 `quick_list` 字段（旧版本），该章节标注 `（待补充——旧版YAML无quick_list字段）`，不影响其他章节

### 第五步：写入输出文件

1. abc-summary.yaml：遵循 yaml-schema.md 中的 abc-summary 格式
2. abc-heatmap.md：Markdown 表格格式，每章一行，包含A/B/C/综合评分
3. abc-quick-list.md：快捷列表汇总，遵循 yaml-schema.md 中的格式规范

### 第六步：完成报告

回复：

"全书汇总完成：
总章节：N
高密度章节：N（XX%）
B合格率：XX%
平均综合评分：X.X
过渡点总数：M 处
峰值章：第X章、第Y章...
问题章：第A章、第B章...

已生成：abc-summary.yaml, abc-heatmap.md, abc-quick-list.md"
```

---

## 主进程调用示例（伪代码）

```python
# 主进程：启动一批 sub-agent
batch_prompt = build_batch_prompt(
    batch_id="batch_1_ch001-005",
    chapter_list=["001", "002", "003", "004", "005"],
    summary_dir=f"{project_dir}/概括/",
    nouns_file=f"{project_dir}/人物和设定/名词表.md",
    abc_def_path=f"{SKILL_DIR}/references/abc-definition.md",
    yaml_schema_path=f"{SKILL_DIR}/references/yaml-schema.md",
    output_dir=f"{project_dir}/ABC分析/"
)

# 使用 ClaudeCode Agent 工具调用
# （在 skill 执行时，这对应 Agent tool 调用）
result = run_agent(
    description="ABC分析批次1(章1-5)",
    prompt=batch_prompt
)
```
