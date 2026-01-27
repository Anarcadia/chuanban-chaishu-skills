# YAML Schema 定义

## 角色地位 (角色地位.yaml)

```yaml
# 角色地位分析
# 用于记录各角色在故事中的重要程度和定位

metadata:
  book: string                      # 书名
  last_processed_chapter: number    # 已处理到的章节
  total_chapters_at_analysis: number # 分析时的总章节数
  last_updated: string              # 最后更新日期

protagonist:
  name: string          # 主角名称
  aliases: [string]     # 别名列表
  importance: number    # 重要程度 1-10

female_leads:           # 女主角列表（按重要程度排序）
  - name: string
    rank: number        # 排名（1=第一女主）
    importance: number  # 重要程度 1-10

male_leads:             # 男主角列表（如有）
  - name: string
    rank: number
    importance: number

antagonists:            # 反派列表
  - name: string
    rank: number        # 排名（1=主要反派）
    importance: number

supporting:             # 重要配角
  - name: string
    importance: number
```

### 示例

```yaml
metadata:
  book: "变身妖女，我靠采补飞升"
  last_processed_chapter: 46
  total_chapters_at_analysis: 46
  last_updated: "2026-01-28"

protagonist:
  name: 宁雨
  aliases: [小萝莉, 杀手]
  importance: 10

female_leads:
  - name: 沈怡月
    rank: 1
    importance: 9
  - name: 宁萱
    rank: 2
    importance: 7

male_leads: []

antagonists:
  - name: 里昂
    rank: 1
    importance: 8
  - name: 晨星
    rank: 2
    importance: 5

supporting:
  - name: 季梦瑶
    importance: 6
  - name: 吴迪
    importance: 5
```

---

## 人物关系 (人物关系.yaml)

```yaml
# 人物关系网
# 记录角色之间的关系

metadata:
  book: string                      # 书名
  last_processed_chapter: number    # 已处理到的章节
  total_chapters_at_analysis: number # 分析时的总章节数
  last_updated: string              # 最后更新日期

relationships:
  protagonist_relations:    # 主角相关关系
    - from: string          # 关系起点
      to: string            # 关系终点
      type: enum            # 关系类型
      description: string   # 关系描述
      key_chapters: [string] # 关键章节

  important_relations:      # 重要配角间关系
    - from: string
      to: string
      type: enum
      description: string

  antagonist_relations:     # 反派相关关系（只记录一层）
    - from: string
      to: string
      type: enum
      description: string
```

### 关系类型 (type) 枚举

| 类型 | 说明 |
|------|------|
| romantic | 恋人/暧昧 |
| family | 家人/亲属 |
| friend | 朋友/队友 |
| enemy | 敌人/对手 |
| subordinate | 上下级 |
| mentor | 师徒 |
| rival | 竞争对手 |

### 示例

```yaml
metadata:
  book: "变身妖女，我靠采补飞升"
  last_processed_chapter: 46
  total_chapters_at_analysis: 46
  last_updated: "2026-01-28"

relationships:
  protagonist_relations:
    - from: 宁雨
      to: 沈怡月
      type: romantic
      description: "恋人，灵魂相依的伙伴"
      key_chapters: ["31-33", "160-162"]
    - from: 宁雨
      to: 宁萱
      type: family
      description: "双胞胎姐妹"
      key_chapters: ["50-52"]

  important_relations:
    - from: 季梦瑶
      to: 吴迪
      type: romantic
      description: "队友发展为恋人"

  antagonist_relations:
    - from: 里昂
      to: 宁萱
      type: subordinate
      description: "宁萱曾是里昂手下"
```

---

## 进度文件 (_progress.json)

```json
{
  "book": "书名",
  "last_processed_chapter": 237,
  "last_processed_group": 79,
  "total_chapters_at_analysis": 237,
  "processed_groups": [1, 3, 7, 13, 15],
  "analysis_rounds": 15,
  "last_updated": "2026-01-28"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| book | string | 书名 |
| last_processed_chapter | number | 最后处理的章节号 |
| last_processed_group | number | 最后处理的组号 |
| total_chapters_at_analysis | number | **分析时的总章节数（用于检测新章节）** |
| processed_groups | [number] | **已分析的组号列表** |
| analysis_rounds | number | 分析轮次 |
| last_updated | string | 最后更新日期 |
