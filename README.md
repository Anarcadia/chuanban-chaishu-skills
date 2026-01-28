# 拆书 Skills 工具包 v1.0

由忒修斯的船板，基于自己的网文小说学习工作流构建的小说拆书分析工具，适用于 Claude Code、Kimi CLI、OpenCode 等 AI 执行的编程自动化终端。

## 功能特性

### 📚 5 个专业 Skills

| Skill | 功能 | 说明 |
|-------|------|------|
| **chai-shu** | 拆书主入口 | 菜单式调度，统一入口 |
| **chai-fen-sao-miao** | 结构扫描 | 识别章节结构，智能拆分 |
| **fen-zhang-jie-gai-kuo** | 分章节概括 | 并行处理，生成章节摘要 |
| **renwu-guanxi** | 人物关系 | 拟人阅读模式，提取人物关系 |
| **shijian-xian** | 事件线追踪 | 拟人确认模式，追踪事件线 |

### 🛠️ Python 工具

- **novel_splitter.py** - 核心拆分工具
  - 支持多种章节格式（卷/部/章/节/话/回/篇/集）
  - 自动识别编码
  - 生成结构化输出

## 快速开始

### 系统要求

- Python 3.7+
- Claude Code / Kimi CLI / OpenCode（任选其一）
- macOS / Linux / Windows

### 安装步骤

#### macOS / Linux

```bash
# 1. 解压工具包
unzip chaishu-skills-v1.0.zip
cd chaishu-skills-v1.0

# 2. 运行安装脚本
./scripts/install.sh

# 3. 按提示输入工作区路径（或直接回车使用默认路径）
```

#### Windows

```powershell
# 1. 解压工具包
# 2. 右键点击 scripts/install.ps1
# 3. 选择"使用 PowerShell 运行"
# 4. 按提示输入工作区路径（或直接回车使用默认路径）
```

### 验证安装

```bash
# macOS / Linux
python3 scripts/verify.py /path/to/your/Root

# Windows
python scripts\verify.py C:\path\to\your\Root
```

## 使用方法

### 方法 1：通过 AI 助手（推荐）

在 Claude Code / Kimi CLI / OpenCode 中输入：

```
拆书
```

会显示交互式菜单，选择需要的功能即可。

### 方法 2：直接使用 Python 工具

```bash
# 扫描小说结构
python3 Factory/拆书/novel_splitter.py --scan 小说.txt

# 拆分小说（按章）
python3 Factory/拆书/novel_splitter.py --split 章 小说.txt

# 查看帮助
python3 Factory/拆书/novel_splitter.py --help
```

## 目录结构

安装后的目录结构：

```
你的工作区/
├── .claude/skills/          # Skills 安装位置
│   ├── chai-shu/
│   ├── chai-fen-sao-miao/
│   ├── fen-zhang-jie-gai-kuo/
│   ├── renwu-guanxi/
│   └── shijian-xian/
│
└── Factory/拆书/             # 拆书工作目录
    ├── novel_splitter.py    # Python 工具
    └── [你的小说文件]
```

## 常见问题

### Q: 支持哪些 AI 编程助手？

A: 支持 Claude Code、Kimi CLI、OpenCode 等使用 `.claude/skills/` 目录的工具。

### Q: 如何卸载？

A: 删除以下目录即可：
- `.claude/skills/chai-shu`
- `.claude/skills/chai-fen-sao-miao`
- `.claude/skills/fen-zhang-jie-gai-kuo`
- `.claude/skills/renwu-guanxi`
- `.claude/skills/shijian-xian`
- `Factory/拆书/novel_splitter.py`

### Q: 安装失败怎么办？

A:
1. 检查 Python 版本是否 3.7+
2. 检查是否有写入权限
3. 运行 `verify.py` 查看具体错误
4. 查看 DEPLOY.md 中的详细说明

### Q: 支持哪些小说格式？

A: 支持 TXT 格式，自动识别编码（UTF-8、GBK 等）。

## 技术支持

- 问题反馈：[GitHub Issues]
- 文档：查看 DEPLOY.md 获取更多技术细节

## 许可证

MIT License - 详见 LICENSE 文件

## 更新日志

### v1.0 (2026-01-28)

- ✨ 首次发布
- 📚 包含 5 个核心 Skills
- 🛠️ 包含 novel_splitter.py 工具
- 🚀 支持 macOS/Linux/Windows
- 📝 完整的安装和验证脚本
