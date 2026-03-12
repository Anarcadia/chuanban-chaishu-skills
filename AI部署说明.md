# 船板拆书 Skill 性能版 v2.0 — AI 部署说明

本文档面向执行部署任务的 AI 助手（Claude / GPT / Gemini 等）。当用户要求你帮助安装和配置"船板拆书 Skill 性能版"时，严格按照以下步骤操作。

---

## 1. Claude Code 安装

船板拆书 Skill 运行在 Claude Code（Anthropic 官方 CLI）之上。部署前必须确保用户环境已安装 Claude Code。

### 1.1 Windows 安装

**前置条件**：
- Node.js 18 或更高版本（推荐 LTS）
- npm（随 Node.js 一同安装）
- 终端：PowerShell 或 Windows Terminal

**安装命令**：
```powershell
npm install -g @anthropic-ai/claude-code
```

**验证安装**：
```powershell
claude --version
```

**常见问题**：

| 问题 | 解决方案 |
|------|----------|
| PowerShell 执行策略限制，提示"无法加载文件...因为在此系统上禁止运行脚本" | 以管理员身份运行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `claude` 命令不存在 | 检查 npm 全局 bin 目录是否在 PATH 中。运行 `npm config get prefix` 查看路径，将其下 `node_modules/.bin` 或根路径加入系统 PATH |
| Node.js 版本过低 | 前往 https://nodejs.org 下载 LTS 版本覆盖安装 |
| npm 权限问题 | 以管理员身份运行 PowerShell，或使用 `npm install -g --prefix %APPDATA%\npm @anthropic-ai/claude-code` |

### 1.2 macOS 安装

**前置条件**：
- Node.js 18 或更高版本（推荐通过 Homebrew 安装）
- npm（随 Node.js 一同安装）

**安装命令**：
```bash
# 如果尚未安装 Node.js
brew install node

# 安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

**验证安装**：
```bash
claude --version
```

**常见问题**：

| 问题 | 解决方案 |
|------|----------|
| 权限报错 `EACCES` | 方案一：`sudo npm install -g @anthropic-ai/claude-code`；方案二（推荐）：修复 npm 全局目录权限 `mkdir ~/.npm-global && npm config set prefix '~/.npm-global'`，然后将 `~/.npm-global/bin` 加入 `~/.zshrc` 的 PATH |
| zsh 找不到 `claude` 命令 | 在 `~/.zshrc` 末尾添加 `export PATH="$(npm config get prefix)/bin:$PATH"`，然后执行 `source ~/.zshrc` |
| Homebrew 未安装 | 执行 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |

---

## 2. Skill 部署

### 2.1 目录结构说明

工具包内包含两个顶级目录：

```
船板拆书skill性能版v2.0/
├── skills/                  # → 部署到 {项目根目录}/.claude/skills/
│   ├── chai-shu/            # 主入口路由
│   ├── chai-fen-sao-miao/   # 拆分扫描
│   ├── fen-zhang-jie-gai-kuo/ # 分章节概括
│   ├── renwu-guanxi/        # 人物关系分析
│   ├── shijian-xian/        # 事件线追踪
│   └── abc-fenxi/           # ABC爽点分析
├── workspace/               # → 部署到用户选择的工作目录
│   ├── novel_splitter.py    # Python拆分脚本（必须）
│   └── CLAUDE.md            # 项目级CLAUDE.md（可选）
└── AI部署说明.md            # 本文档
```

**关键术语定义**：
- **项目根目录**：用户运行 `claude` 命令时所在的目录，即 Claude Code 会话的工作目录根。该目录下应存在或将创建 `.claude/` 隐藏目录。
- **工作目录**：`novel_splitter.py` 脚本存放的位置。拆分出的小说章节文件默认写入此目录的子目录。

### 2.2 部署步骤

以下步骤需要你（AI 助手）协助用户完成。先向用户确认两个路径：

1. **项目根目录**（以下记为 `PROJECT_ROOT`）——用户打算在哪个目录下使用 Claude Code
2. **工作目录**（以下记为 `WORK_DIR`）——用户希望把待拆书籍和拆分结果存放在哪里

#### 步骤 1：部署 Skills（必须）

将 `skills/` 下的全部 6 个子目录复制到 `{PROJECT_ROOT}/.claude/skills/`。

**macOS / Linux**：
```bash
# 确保目标目录存在
mkdir -p "{PROJECT_ROOT}/.claude/skills"

# 复制全部 6 个 skill 目录
cp -r skills/chai-shu "{PROJECT_ROOT}/.claude/skills/"
cp -r skills/chai-fen-sao-miao "{PROJECT_ROOT}/.claude/skills/"
cp -r skills/fen-zhang-jie-gai-kuo "{PROJECT_ROOT}/.claude/skills/"
cp -r skills/renwu-guanxi "{PROJECT_ROOT}/.claude/skills/"
cp -r skills/shijian-xian "{PROJECT_ROOT}/.claude/skills/"
cp -r skills/abc-fenxi "{PROJECT_ROOT}/.claude/skills/"
```

**Windows PowerShell**：
```powershell
# 确保目标目录存在
New-Item -ItemType Directory -Force -Path "{PROJECT_ROOT}\.claude\skills"

# 复制全部 6 个 skill 目录
Copy-Item -Recurse -Force "skills\chai-shu" "{PROJECT_ROOT}\.claude\skills\"
Copy-Item -Recurse -Force "skills\chai-fen-sao-miao" "{PROJECT_ROOT}\.claude\skills\"
Copy-Item -Recurse -Force "skills\fen-zhang-jie-gai-kuo" "{PROJECT_ROOT}\.claude\skills\"
Copy-Item -Recurse -Force "skills\renwu-guanxi" "{PROJECT_ROOT}\.claude\skills\"
Copy-Item -Recurse -Force "skills\shijian-xian" "{PROJECT_ROOT}\.claude\skills\"
Copy-Item -Recurse -Force "skills\abc-fenxi" "{PROJECT_ROOT}\.claude\skills\"
```

部署后目录结构应为：
```
{PROJECT_ROOT}/
└── .claude/
    └── skills/
        ├── chai-shu/
        │   ├── SKILL.md
        │   └── references/
        │       └── quickstart.md
        ├── chai-fen-sao-miao/
        │   └── SKILL.md
        ├── fen-zhang-jie-gai-kuo/
        │   ├── SKILL.md
        │   └── references/
        │       ├── workflow.md
        │       └── sub-agent-prompt.md
        ├── renwu-guanxi/
        │   ├── SKILL.md
        │   └── references/
        │       ├── workflow.md
        │       └── yaml-schema.md
        ├── shijian-xian/
        │   ├── SKILL.md
        │   └── references/
        │       ├── workflow.md
        │       └── yaml-schema.md
        └── abc-fenxi/
            ├── skill.md
            └── references/
                ├── abc-definition.md
                ├── workflow.md
                ├── sub-agent-prompt.md
                └── yaml-schema.md
```

#### 步骤 2：部署 Python 脚本（必须）

将 `workspace/novel_splitter.py` 复制到工作目录。

**macOS / Linux**：
```bash
cp workspace/novel_splitter.py "{WORK_DIR}/"
```

**Windows PowerShell**：
```powershell
Copy-Item "workspace\novel_splitter.py" "{WORK_DIR}\"
```

#### 步骤 3：部署项目 CLAUDE.md（可选）

`workspace/CLAUDE.md` 包含拆书系统的项目概述和目录结构规范。如果用户的项目根目录下尚无 `CLAUDE.md`，可将其复制过去；如已有，可将内容追加或合并。

**macOS / Linux**：
```bash
# 情况A：用户没有现成的 CLAUDE.md → 直接复制
cp workspace/CLAUDE.md "{PROJECT_ROOT}/CLAUDE.md"

# 情况B：用户已有 CLAUDE.md → 追加内容
cat workspace/CLAUDE.md >> "{PROJECT_ROOT}/CLAUDE.md"
```

**Windows PowerShell**：
```powershell
# 情况A：用户没有现成的 CLAUDE.md → 直接复制
Copy-Item "workspace\CLAUDE.md" "{PROJECT_ROOT}\CLAUDE.md"

# 情况B：用户已有 CLAUDE.md → 追加内容
Get-Content "workspace\CLAUDE.md" | Add-Content "{PROJECT_ROOT}\CLAUDE.md"
```

### 2.3 路径占位符替换

Skill 文件内部使用了以下占位符，部署后必须替换为用户的实际路径：

| 占位符 | 含义 | 替换为 |
|--------|------|--------|
| `{ROOT}` | 项目根目录 | 用户的 `PROJECT_ROOT` 绝对路径 |
| `{WORKSPACE}` | 工作目录（novel_splitter.py 所在位置） | 用户的 `WORK_DIR` 绝对路径 |
| `{HOME}` | 用户主目录 | 系统 HOME 目录绝对路径 |

**需要替换的文件列表**（相对于 `{PROJECT_ROOT}/.claude/skills/`）：

- `chai-shu/SKILL.md` — 包含 `{ROOT}`
- `chai-shu/references/quickstart.md` — 包含 `{ROOT}`
- `chai-fen-sao-miao/SKILL.md` — 包含 `{WORKSPACE}`
- `fen-zhang-jie-gai-kuo/SKILL.md` — 包含 `{ROOT}`
- `fen-zhang-jie-gai-kuo/references/workflow.md` — 包含 `{ROOT}`
- `renwu-guanxi/SKILL.md` — 包含 `{ROOT}`
- `renwu-guanxi/references/workflow.md` — 包含 `{ROOT}`
- `shijian-xian/SKILL.md` — 包含 `{ROOT}`
- `shijian-xian/references/workflow.md` — 包含 `{ROOT}`
- `abc-fenxi/skill.md` — 包含 `{ROOT}`
- `abc-fenxi/references/workflow.md` — 包含 `{ROOT}`

**macOS / Linux 批量替换命令**：

```bash
# 定义用户实际路径（替换下方值）
PROJECT_ROOT="/Users/用户名/实际项目路径"
WORK_DIR="/Users/用户名/实际工作目录路径"
HOME_DIR="$HOME"

SKILLS_DIR="$PROJECT_ROOT/.claude/skills"

# 替换 {ROOT}
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{ROOT}|$PROJECT_ROOT|g" {} +

# 替换 {WORKSPACE}
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{WORKSPACE}|$WORK_DIR|g" {} +

# 替换 {HOME}（如果存在）
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{HOME}|$HOME_DIR|g" {} +
```

**Windows PowerShell 批量替换命令**：

```powershell
# 定义用户实际路径（替换下方值）
$PROJECT_ROOT = "C:\Users\用户名\实际项目路径"
$WORK_DIR = "C:\Users\用户名\实际工作目录路径"
$HOME_DIR = $env:USERPROFILE

$SKILLS_DIR = "$PROJECT_ROOT\.claude\skills"

# 遍历所有 .md 文件执行替换
Get-ChildItem -Path $SKILLS_DIR -Filter "*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $content = $content -replace [regex]::Escape('{ROOT}'), $PROJECT_ROOT.Replace('\', '/')
    $content = $content -replace [regex]::Escape('{WORKSPACE}'), $WORK_DIR.Replace('\', '/')
    $content = $content -replace [regex]::Escape('{HOME}'), $HOME_DIR.Replace('\', '/')
    Set-Content -Path $_.FullName -Value $content -Encoding UTF8 -NoNewline
}
```

**注意**：Windows 路径替换时统一转为正斜杠 `/`（Claude Code 在所有平台上均兼容正斜杠），避免反斜杠在正则或 Markdown 中引发转义问题。

### 2.4 部署验证清单

部署完成后，执行以下检查确认一切就绪：

1. **Skill 识别验证**：在项目根目录启动 Claude Code，输入 `拆书`，应看到拆书主入口的 ASCII 欢迎页
2. **Python 脚本验证**：
   ```bash
   python3 "{WORK_DIR}/novel_splitter.py" --help
   ```
   应输出 argparse 帮助信息，包含 `--scan`、`--split`、`--output`、`--json` 等参数
3. **路径替换验证**：抽查任意一个 skill 文件，确认不含 `{ROOT}`、`{WORKSPACE}`、`{HOME}` 占位符：
   ```bash
   grep -r '{ROOT}\|{WORKSPACE}\|{HOME}' "{PROJECT_ROOT}/.claude/skills/"
   ```
   预期输出为空（无匹配）

---

## 3. 各 Skill 功能概述

| Skill 名称 | 功能 | 执行模式 | 关键输出 |
|------------|------|----------|----------|
| `chai-shu` | 主入口路由器，提供功能菜单，根据用户选择分发到对应子 skill | 菜单驱动，纯路由 | 无直接文件输出，负责调度 |
| `chai-fen-sao-miao` | 章节拆分：扫描小说文件结构 + 按用户指定层级执行拆分 | 调用 `novel_splitter.py`，扫描后等待用户确认拆分层级再执行 | `{书名}/拆分/` 目录，内含 `001_第一章_xxx.md` 格式的章节文件 |
| `fen-zhang-jie-gai-kuo` | 分章节概括：每 3 章一组，串行生成约 500 字剧情概括 | 严格串行 sub-agent（禁止并行），滚动上下文 + 断点续传 | `{书名}/概括/` 目录，内含 `组N_第X-Y章_概括.md`；附带 `_progress.json` 进度文件 |
| `renwu-guanxi` | 人物关系分析：模拟阅读过程，先假设后验证，梳理全书角色 | 拟人阅读模式，带笔记归纳 | `{书名}/人物和设定/` 目录，内含 `角色地位.yaml`、`人物关系.yaml`、`关系图谱.md`、`名词表.md` |
| `shijian-xian` | 事件线追踪：提炼关键事件链、势力动向与因果逻辑 | 拟人确认模式（梳理→审视→有疑问回原文确认） | `{书名}/事件线/` 目录，内含 `事件线.yaml`、`时间轴.md` |
| `abc-fenxi` | ABC 爽点分析：识别每章 A（动机共情）/ B（装逼反应）/ C（嵌套突然）结构 | 并行 sub-agent（默认 3 章一批） | `{书名}/ABC分析/` 目录，内含 `abc-ch{XXX}.yaml`（逐章）、`abc-summary.yaml`（汇总）、`abc-heatmap.md`（热力图）、`abc-quick-list.md`（快捷列表） |

**功能依赖链**：

```
chai-fen-sao-miao（拆分扫描）
        │
        v
fen-zhang-jie-gai-kuo（分章节概括）
        │
        ├──→ renwu-guanxi（人物关系）
        ├──→ shijian-xian（事件线）
        └──→ abc-fenxi（ABC分析）
```

功能 3（分章节概括）依赖功能 2（拆分扫描）的输出；功能 4-7 均依赖功能 3 的输出。执行前必须检查前置依赖是否已完成，如未完成应提示用户先执行前置步骤。

**自动化拆书模式**：按顺序执行 拆分扫描 → 分章节概括 → 人物概括 → 事件概括 → ABC 分析。

---

## 4. 依赖说明

### 4.1 Python 依赖

`novel_splitter.py` 使用的库：

| 库名 | 来源 | 用途 |
|------|------|------|
| `pathlib` | 标准库 | 路径操作 |
| `re` | 标准库 | 正则表达式匹配章节标题 |
| `argparse` | 标准库 | 命令行参数解析 |
| `json` | 标准库 | JSON 格式输出 |
| `shutil` | 标准库 | 文件移动操作 |
| `os` | 标准库 | 系统路径操作 |
| `unicodedata` | 标准库 | Unicode 字符规范化 |
| `chardet` | **需 pip 安装** | 文件编码自动检测 |

**安装第三方依赖**：
```bash
# macOS / Linux
pip3 install chardet

# Windows
pip install chardet
```

Python 版本要求：3.6 或更高。

**无其他第三方 Python 包依赖。**

### 4.2 Claude Code 依赖

Skill 运行时依赖以下 Claude Code 内置功能：

| 功能 | 用途 | 说明 |
|------|------|------|
| Agent 工具（sub-agent） | 分章节概括和 ABC 分析使用 sub-agent 执行分组任务 | Claude Code 内置，无需额外配置 |
| Glob | 文件搜索、定位章节文件 | Claude Code 内置 |
| Grep | 文本搜索 | Claude Code 内置 |
| Read | 读取章节文件内容 | Claude Code 内置 |
| Write | 写入概括、分析结果文件 | Claude Code 内置 |
| Edit | 编辑已有文件 | Claude Code 内置 |
| Bash | 执行 Python 脚本 | Claude Code 内置 |

**不依赖任何外部 MCP 服务。** 所有功能完全在本地运行。

---

## 5. 疑难排解

### 5.1 novel_splitter.py 无法运行

**症状**：执行 `python3 novel_splitter.py --scan "文件路径"` 时报错。

**排查步骤**：

1. **检查 Python 版本**：
   ```bash
   python3 --version    # macOS / Linux
   python --version     # Windows
   ```
   要求 3.6 或更高。如果版本过低，升级 Python。

2. **检查脚本路径**：确认 `novel_splitter.py` 在预期位置。执行时使用绝对路径：
   ```bash
   python3 "/绝对路径/novel_splitter.py" --scan "小说文件路径"
   ```

3. **Windows 特殊处理**：Windows 上通常使用 `python` 而非 `python3`：
   ```powershell
   python "C:\绝对路径\novel_splitter.py" --scan "小说文件路径"
   ```

4. **chardet 缺失报错**（`ModuleNotFoundError: No module named 'chardet'`）：见 5.5 节。

5. **兜底方案——手动拆分**：如果 Python 脚本始终无法运行，可由 AI 助手手动完成拆分：
   - 用 Read 工具读取小说文件
   - 用 Grep 搜索章节标题模式（如 `^第.+章`）
   - 按匹配结果手动切分内容
   - 写入 `{书名}/拆分/` 目录，命名格式：`{三位序号}_{章节标题}.md`（如 `001_第一章_重生.md`）

### 5.2 sub-agent 超时或返回空结果

**症状**：分章节概括或 ABC 分析执行时，sub-agent 长时间无响应或返回空内容。

**排查步骤**：

1. **检查 Claude Code 版本**：
   ```bash
   claude --version
   ```
   确保使用最新稳定版。如有更新可用：
   ```bash
   npm update -g @anthropic-ai/claude-code
   ```

2. **检查 API 额度**：确认 Anthropic API key 有效且余额充足。sub-agent 每次调用都消耗 token。

3. **降低并行度**：
   - `abc-fenxi`（ABC 分析）默认使用并行 sub-agent。如果频繁超时，可在对话中指示 Claude 改为逐章串行分析，而非批量并行。
   - `fen-zhang-jie-gai-kuo`（分章节概括）本身已是严格串行，若仍超时，考虑减少单组章节数（从 3 章改为 2 章）。

4. **重试机制**：单次 sub-agent 失败后，直接重新发起该组任务。分章节概括支持断点续传（见 5.4 节），无需从头开始。

### 5.3 路径替换后仍报错

**症状**：已完成 2.3 节的占位符替换，但执行时仍提示文件找不到或路径错误。

**排查步骤**：

1. **确认使用绝对路径**：所有路径必须是绝对路径，不得使用 `~` 或相对路径。
   - 正确：`/Users/zhangsan/projects/novels`
   - 错误：`~/projects/novels`、`./novels`

2. **确认目录实际存在**：
   ```bash
   ls -la "/替换后的路径/"
   ```
   如果目录不存在，先创建：
   ```bash
   mkdir -p "/替换后的路径/Factory/拆书"
   ```

3. **Windows 路径格式**：
   - 推荐使用正斜杠：`C:/Users/zhangsan/projects`
   - 如果使用反斜杠，必须双写：`C:\\Users\\zhangsan\\projects`
   - 避免路径中包含中文空格（如有，用双引号包裹完整路径）

4. **检查残余占位符**：
   ```bash
   grep -r '{ROOT}\|{WORKSPACE}\|{HOME}' "{PROJECT_ROOT}/.claude/skills/"
   ```
   如有输出，说明替换不完整，需对未替换的文件重新执行替换。

### 5.4 断点续传不工作

**症状**：分章节概括中断后重新启动，未能从断点继续，而是从头开始。

**排查步骤**：

1. **检查进度文件是否存在**：
   ```bash
   ls "{书名}/概括/_progress.json"
   ```
   如果文件不存在，说明上次执行未生成进度记录，只能从头开始。

2. **检查进度文件格式**：进度文件应为合法 JSON。用以下命令验证：
   ```bash
   python3 -c "import json; json.load(open('{书名}/概括/_progress.json'))"
   ```
   如果报错，说明 JSON 格式损坏。

3. **手动修复进度文件**：如果文件损坏，根据 `概括/` 目录下已有的概括文件手动重建。标准格式示例：
   ```json
   {
     "total_groups": 16,
     "completed_groups": [1, 2, 3, 4, 5],
     "current_group": 6,
     "last_group_summary": "（第5组概括的最后一段摘要文本）"
   }
   ```
   其中 `completed_groups` 列出所有已完成的组编号，`current_group` 为下一个待处理的组编号。

4. **手动触发续传**：在 Claude Code 中使用以下句式：
   ```
   请继续这个拆书项目。
   源项目目录：{书名目录的绝对路径}
   任务：分章节概括
   ```

### 5.5 chardet 未安装

**症状**：运行 `novel_splitter.py` 时报错 `ModuleNotFoundError: No module named 'chardet'`。

**解决方案**：

```bash
# macOS / Linux
pip3 install chardet

# Windows
pip install chardet

# 如果 pip 版本与 Python 版本不对应，使用：
python3 -m pip install chardet   # macOS / Linux
python -m pip install chardet    # Windows
```

**兜底方案**：如果无法安装 chardet（如受限环境），`novel_splitter.py` 内置了编码降级逻辑——在 chardet 检测失败时，会依次尝试 `utf-8`、`gbk`、`gb2312`、`gb18030` 编码加载文件。但此降级逻辑仅在 `chardet.detect()` 返回结果后的 `_load_text()` 异常分支中生效。

如果连 `import chardet` 都失败（即模块完全不存在），需要修改脚本第 15 行，将：
```python
import chardet
```
改为：
```python
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False
```
并修改 `detect_encoding` 方法，在 `HAS_CHARDET` 为 `False` 时直接返回 `'utf-8'`：
```python
def detect_encoding(self) -> str:
    if not HAS_CHARDET:
        return 'utf-8'
    with open(self.file_path, 'rb') as f:
        raw = f.read(10000)
        result = chardet.detect(raw)
        return result['encoding'] or 'utf-8'
```

此修改后，脚本在无 chardet 环境下仍可运行，但编码检测能力降级为默认 UTF-8（对 GBK 编码的文件需手动转码后再处理）。

---

## 附录 A：完整部署快速命令（macOS 一键脚本）

将以下内容保存为 `deploy.sh` 并执行，可一步完成部署和路径替换：

```bash
#!/bin/bash
set -e

# ====== 用户配置区（修改这三行） ======
PROJECT_ROOT="/Users/你的用户名/你的项目目录"
WORK_DIR="/Users/你的用户名/你的工作目录"
TOOL_PACK="/Users/你的用户名/Downloads/船板拆书skill性能版v2.0"
# ======================================

SKILLS_DIR="$PROJECT_ROOT/.claude/skills"

echo "=== 船板拆书 Skill v2.0 部署脚本 ==="

# 1. 创建目标目录
mkdir -p "$SKILLS_DIR"
mkdir -p "$WORK_DIR"

# 2. 复制 skills
for skill in chai-shu chai-fen-sao-miao fen-zhang-jie-gai-kuo renwu-guanxi shijian-xian abc-fenxi; do
    cp -r "$TOOL_PACK/skills/$skill" "$SKILLS_DIR/"
    echo "  已部署: $skill"
done

# 3. 复制 Python 脚本
cp "$TOOL_PACK/workspace/novel_splitter.py" "$WORK_DIR/"
echo "  已部署: novel_splitter.py"

# 4. 路径替换
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{ROOT}|$PROJECT_ROOT|g" {} +
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{WORKSPACE}|$WORK_DIR|g" {} +
find "$SKILLS_DIR" -name "*.md" -exec sed -i '' "s|{HOME}|$HOME|g" {} +
echo "  路径替换完成"

# 5. 验证
REMAINING=$(grep -rl '{ROOT}\|{WORKSPACE}\|{HOME}' "$SKILLS_DIR" 2>/dev/null || true)
if [ -z "$REMAINING" ]; then
    echo "=== 部署成功！无残余占位符 ==="
else
    echo "=== 警告：以下文件仍含占位符 ==="
    echo "$REMAINING"
fi

# 6. 检查 chardet
python3 -c "import chardet" 2>/dev/null && echo "  chardet: 已安装" || echo "  警告: chardet 未安装，请执行 pip3 install chardet"

echo "=== 部署完毕 ==="
```

## 附录 B：完整部署快速命令（Windows PowerShell 脚本）

将以下内容保存为 `deploy.ps1` 并在 PowerShell 中执行：

```powershell
# ====== 用户配置区（修改这三行） ======
$PROJECT_ROOT = "C:\Users\你的用户名\你的项目目录"
$WORK_DIR = "C:\Users\你的用户名\你的工作目录"
$TOOL_PACK = "C:\Users\你的用户名\Downloads\船板拆书skill性能版v2.0"
# ======================================

$SKILLS_DIR = "$PROJECT_ROOT\.claude\skills"

Write-Host "=== 船板拆书 Skill v2.0 部署脚本 ==="

# 1. 创建目标目录
New-Item -ItemType Directory -Force -Path $SKILLS_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $WORK_DIR | Out-Null

# 2. 复制 skills
$skills = @("chai-shu", "chai-fen-sao-miao", "fen-zhang-jie-gai-kuo", "renwu-guanxi", "shijian-xian", "abc-fenxi")
foreach ($skill in $skills) {
    Copy-Item -Recurse -Force "$TOOL_PACK\skills\$skill" "$SKILLS_DIR\"
    Write-Host "  已部署: $skill"
}

# 3. 复制 Python 脚本
Copy-Item "$TOOL_PACK\workspace\novel_splitter.py" "$WORK_DIR\"
Write-Host "  已部署: novel_splitter.py"

# 4. 路径替换（统一转正斜杠）
$PR = $PROJECT_ROOT.Replace('\', '/')
$WD = $WORK_DIR.Replace('\', '/')
$HD = $env:USERPROFILE.Replace('\', '/')

Get-ChildItem -Path $SKILLS_DIR -Filter "*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $content = $content -replace [regex]::Escape('{ROOT}'), $PR
    $content = $content -replace [regex]::Escape('{WORKSPACE}'), $WD
    $content = $content -replace [regex]::Escape('{HOME}'), $HD
    Set-Content -Path $_.FullName -Value $content -Encoding UTF8 -NoNewline
}
Write-Host "  路径替换完成"

# 5. 检查 chardet
try {
    python -c "import chardet" 2>$null
    Write-Host "  chardet: 已安装"
} catch {
    Write-Host "  警告: chardet 未安装，请执行 pip install chardet"
}

Write-Host "=== 部署完毕 ==="
```

---

## 附录 C：Skill 触发方式速查

在 Claude Code 中使用以下自然语言即可触发对应 skill：

| 触发词 | 触发的 Skill |
|--------|-------------|
| "拆书"、"分析小说"、"小说拆解" | `chai-shu`（主入口） |
| "拆分扫描"、"扫描小说结构"、"拆分章节" | `chai-fen-sao-miao` |
| "分章节概括"、"章节概括"、"逐章概括" | `fen-zhang-jie-gai-kuo` |
| "人物概括"、"人物关系"、"角色分析" | `renwu-guanxi` |
| "事件概括"、"事件线"、"时间轴" | `shijian-xian` |
| "ABC分析"、"爽点分析"、"ABC结构" | `abc-fenxi` |

推荐通过主入口 `拆书` 触发，由路由菜单引导选择具体功能。

---

*本文档版本：v2.0 | 适用于船板拆书 Skill 性能版 v2.0*
