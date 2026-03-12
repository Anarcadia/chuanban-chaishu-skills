# YAML 输出格式规范

> 版本：v1.0（2026-03-11）

---

## 单章分析文件（abc-ch{XXX}.yaml）

### 命名规则
- 格式：`abc-ch{章节序号}.yaml`
- 序号：3位补零（001, 002, ... 100）
- 位置：`{书名}/ABC分析/`

### 字段规范

```yaml
# --- 必填元信息 ---
chapter_id: "001"                    # STRING, 3位补零
chapter_title: "（章节标题）"         # STRING, 从概括文件提取
source_summary_file: "概括/组1_第1-3章_概括.md"  # STRING, 来源文件名
analyzed_at: "YYYY-MM-DD"           # DATE
model_used: "claude-sonnet-4-6"     # STRING

# --- ABC循环列表 ---
abc_cycles:                          # LIST, 1-3个循环
  - cycle_id: 1                      # INTEGER, 从1开始
    level: main                      # ENUM: main | sub | micro
    summary: "（一句话描述本循环内容）"  # STRING, ≤50字

    A:
      content: "（A的情节内容描述）"   # STRING, ≤100字
      intensity: 4                   # INTEGER 1-5
      共情类型: 弱者共情               # ENUM: 弱者共情|能力暗示|目标铺垫|矛盾落差
      铺垫手段:                       # LIST, 1-5条
        - "（铺垫手段1）"
      期待感: "（对读者期待感的评估）"  # STRING, ≤50字

    B:
      装逼:
        content: "（装逼行为描述）"    # STRING, ≤80字
        intensity: 3                 # INTEGER 1-5
      反应:
        content: "（反应的总体描述）"  # STRING, ≤100字
        intensity: 4                 # INTEGER 1-5
        反应篇幅比: 2.5              # FLOAT, 反应字数/装逼字数，目标≥2.0
        分层:                        # LIST, 至少2层（合格标准）
          - 层级: 质疑者              # ENUM: 质疑者|围观群众|嘲讽者|强者重评|扩散效应
            内容: "（具体反应描述）"   # STRING
        B完整度: 合格                # ENUM: 合格|不合格

    C:
      content: "（C的内容描述）"      # STRING, ≤80字
      intensity: 4                   # INTEGER 1-5
      类型: 突然                     # ENUM: 突然|嵌套|规模扩大
      下一循环预埋: "（下一章A的伏笔）" # STRING, 可null
      cross_chapter_note: null       # STRING|null, 大循环节点说明

    self_review_notes: "（自审发现和修改记录）"  # STRING

# --- 快捷列表（必填）---
quick_list:                          # LIST, 5-15条，按情节时间顺序排列
  - seq: 1                          # INTEGER, 从1开始，按时间顺序递增
    plot: "（情节描述）"              # STRING, ≤30字
    tag: "A"                         # ENUM: A|B|A2|B2|A3|B3|B→A'⟳|C
    note: "（功能说明）"              # STRING, ≤20字
  - seq: 2
    plot: "（情节描述）"
    tag: "B"
    note: "（功能说明）"
  # ... 5-15条

# --- 章节综合评估（必填）---
chapter_summary:
  abc_density: 中                   # ENUM: 高|中|低
  structure_quality: 3.5            # FLOAT 1.0-5.0
  main_cycle_b_quality: 合格        # ENUM: 合格|不合格
  weak_points:                      # LIST, 0-5条
    - "（具体问题描述）"
  suggestions:                      # LIST, 0-5条
    - "（具体改进建议）"
  overall_note: "（总体评价）"       # STRING, ≤100字
```

### 字段允许值速查

| 字段 | 允许值 |
|------|--------|
| level | `main` / `sub` / `micro` |
| A.共情类型 | `弱者共情` / `能力暗示` / `目标铺垫` / `矛盾落差` |
| B.反应.分层[].层级 | `质疑者` / `围观群众` / `嘲讽者` / `强者重评` / `扩散效应` |
| B.反应.B完整度 | `合格`（反应层级≥2且篇幅比≥1.5）/ `不合格` |
| C.类型 | `突然` / `嵌套` / `规模扩大` |
| quick_list[].tag | `A` / `B` / `A2` / `B2` / `A3` / `B3` / `B→A'⟳` / `C` |
| chapter_summary.abc_density | `高` / `中` / `低` |

### 密度判定规则

```
abc_density 判定：
  高：A intensity≥3 AND B完整度=合格 AND C intensity≥2
  低：B完整度=不合格 OR (A intensity≤2 AND C intensity≤1)
  中：其他情况

structure_quality 计算：
  基础分 = (A_intensity + B装逼_intensity + B反应_intensity + C_intensity) / 4
  扣分：B完整度=不合格 → -0.5
  加分：反应篇幅比≥3.0 → +0.3
```

---

## 全书汇总文件（abc-summary.yaml）

```yaml
book_title: "（书名）"               # STRING
analyzed_at: "YYYY-MM-DD"           # DATE
total_chapters: 50                  # INTEGER
analyzed_chapters: 50               # INTEGER

overall_metrics:
  high_density_count: N             # INTEGER
  medium_density_count: N           # INTEGER
  low_density_count: N              # INTEGER
  abc_density_ratio: "XX%"          # STRING, 高密度占比
  avg_structure_quality: X.X        # FLOAT
  b_reaction_pass_rate: "XX%"       # STRING, B合格率

top_chapters:                       # LIST, 最多5章
  - chapter_id: "015"
    title: "（章节标题）"
    reason: "（爽点突出原因，≤80字）"
    structure_quality: X.X

weak_chapters:                      # LIST, 最多5章
  - chapter_id: "008"
    title: "（章节标题）"
    reason: "（问题描述，≤80字）"
    structure_quality: X.X
    suggestion: "（改进建议，≤100字）"

pacing_analysis:
  rhythm_pattern: "（整体节奏描述，≤100字）"
  dry_spells:                       # LIST, 连续3+章低密度区间
    - chapters: "ch018-ch022"       # STRING
      suggestion: "（改善建议）"

b_reaction_analysis:
  avg_reaction_ratio: X.X           # FLOAT
  most_common_issue: "（最常见B问题）"
  pass_count: N
  fail_count: N

c_hook_analysis:
  chapters_with_hook: N
  chapters_without_hook: N
  most_effective_c_type: "（最有效的C类型）"
```

---

## 进度文件（_progress.json）

```json
{
  "book": "书名",
  "project_dir": "/absolute/path/to/book/",
  "total_chapters": 50,
  "analyzed_chapters": ["001", "002", "003"],
  "failed_chapters": [],
  "last_updated": "2026-03-11",
  "batches_completed": [
    "batch_1_ch001-005",
    "batch_2_ch006-010"
  ],
  "summary_generated": false
}
```

---

## 快捷列表汇总文件（abc-quick-list.md）

由汇总 sub-agent 遍历所有章节 YAML 的 `quick_list` 字段，按章节顺序拼接生成。

### 格式规范

```markdown
# ABC快捷列表 — 《书名》

> 生成日期：YYYY-MM-DD
> 总章节：N 章 | 过渡点：M 处

## 第1章 （章节标题）

| # | 情节 | 标记 | 说明 |
|---|------|------|------|
| 1 | 主角被当众羞辱 | A | 弱者共情铺垫 |
| 2 | 主角亮出隐藏实力 | B | 逆转打脸 |
| 3 | 嘲讽者震惊失色 | B | 反应第1层 |
| 4 | 强者重新审视主角 | B→A'⟳ | 过渡：强者重评+收徒派任务 |
| 5 | 章末新威胁出现 | C | 结尾钩子 |

## 第2章 （章节标题）

| # | 情节 | 标记 | 说明 |
|---|------|------|------|
| ... | ... | ... | ... |

---

**标记说明**：
- A/A2/A3 = 动机共情（第1/2/3循环）
- B/B2/B3 = 装逼反应（第1/2/3循环）
- B→A'⟳ = 过渡点（当前循环收尾 + 下一循环开始）
- C = 嵌套/突然/钩子
```

### 兼容规则

- 旧 YAML（无 `quick_list` 字段）：该章节在汇总文件中标注 `（待补充——旧版YAML无quick_list字段）`
- 不影响其他章节的正常拼接
