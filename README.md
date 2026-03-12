# 拆书 Skills 工具包 v2.2

由忒修斯的船板 (Anarcadia) 构建的小说拆书分析工具，适用于 Claude Code、Kimi CLI、OpenCode 等 AI 编程终端。

**一句话版本**：让 AI 帮你把一本网文拆成结构化分析报告——章节概括、人物关系、事件线、爽点分析，全都自动生成。

## 功能特性

### 📚 6 个专业 Skills

| Skill | 功能 | 说明 |
|-------|------|------|
| **chai-shu** | 拆书主入口 | 菜单式调度，统一入口，阶段衔接协议 |
| **chai-fen-sao-miao** | 结构扫描 | 识别章节结构，智能拆分 |
| **fen-zhang-jie-gai-kuo** | 分章节概括 | 串行 sub-agent 架构，每3章一组生成500字概括 |
| **renwu-guanxi** | 人物关系 | 拟人阅读模式，角色地位 + 关系图谱 |
| **shijian-xian** | 事件线追踪 | 拟人确认模式，主线 + 支线事件链 |
| **abc-fenxi** | ABC爽点分析 | 并行批处理，爽点密度热力图 |

### 🛠️ Python 工具

- **novel_splitter.py** - 核心拆分脚本
  - 支持多种章节格式（卷/部/章/节/话/回/篇/集）
  - 自动识别编码（依赖 chardet）
  - 生成结构化输出

## 核心流程

```
       你的小说文件（.txt）
              │
              v
     ┌────────────────┐
     │  1. 拆分扫描    │
     └────────┬───────┘
              │
              v
     ┌────────────────┐
     │  2. 分章节概括   │
     └───┬────┬────┬──┘
         │    │    │
         v    v    v      （三条线可以独立跑，互不影响）
    ┌────┐ ┌────┐ ┌────┐
    │人物│ │事件│ │ABC │
    │概括│ │概括│ │分析│
    └────┘ └────┘ └────┘
```

## 快速开始

### 系统要求

- Python 3.6+（需 `pip install chardet`）
- Claude Code（Anthropic 官方 CLI）
- macOS / Linux / Windows

### 安装

详见 **[AI部署说明.md](AI部署说明.md)** — 面向 AI 助手的完整部署指南，包含：
- Claude Code 安装（Windows/macOS）
- Skill 部署步骤
- 路径占位符替换
- 一键部署脚本（macOS + Windows）
- 疑难排解

### 使用

详见 **[用户指南.md](用户指南.md)** — 面向用户的完整使用说明，包含：
- 每个步骤的详细解说
- 产出文件示例
- ABC 爽点分析法讲解
- 常见问题解答

### 快速示例

在 Claude Code 中输入：

```
拆书
```

会显示交互式菜单。或者直接：

```
请帮我拆书。
任务：自动化拆书。
输入书籍：/path/to/your/novel.txt
```

## 目录结构

```
本仓库/
├── skills/                     # Skill 文件（部署到 .claude/skills/）
│   ├── chai-shu/               # 主入口路由
│   ├── chai-fen-sao-miao/      # 拆分扫描
│   ├── fen-zhang-jie-gai-kuo/  # 分章节概括
│   ├── renwu-guanxi/           # 人物关系分析
│   ├── shijian-xian/           # 事件线追踪
│   └── abc-fenxi/              # ABC爽点分析
├── workspace/                  # 工作区文件
│   ├── novel_splitter.py       # Python拆分脚本
│   └── CLAUDE.md               # 项目级配置模板
├── 用户指南.md                  # 用户使用说明
├── AI部署说明.md                # AI助手部署指南
└── README.md
```

## v2.2 更新内容

相比 v1.0：
- ✨ 新增 ABC 爽点分析 skill（并行批处理架构）
- ✨ 新增阶段衔接协议（子阶段完成后自动呈现下一步选项）
- ✨ 新增编排模式（子 skill 被主入口调用时跳过欢迎页、返回状态摘要）
- ✨ 新增续接状态综合判断（5步状态表格 + 智能推荐）
- 🔧 分章节概括改为串行 sub-agent 架构（性能版优化）
- 🔧 人物/事件概括改为拟人阅读/确认模式
- 📝 新增完整用户指南和 AI 部署说明
- 🗑️ 移除旧版安装脚本和验证工具（改用 AI 辅助部署）

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 技术支持

- 问题反馈：[GitHub Issues](https://github.com/Anarcadia/chuanban-chaishu-skills/issues)
