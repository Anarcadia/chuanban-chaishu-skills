# 拆书 Skills 部署指南（AI 版本）

本文档面向 AI 助手，提供详细的部署和故障排查指南。

## 部署架构

### 文件结构

```
chaishu-skills-v1.0/
├── skills/                  # Skills 源文件（含占位符）
│   ├── chai-shu/
│   │   └── SKILL.md        # 主入口，菜单调度
│   ├── chai-fen-sao-miao/
│   │   └── SKILL.md        # 结构扫描与拆分
│   ├── fen-zhang-jie-gai-kuo/
│   │   ├── SKILL.md        # 分章节概括（主调度）
│   │   └── references/
│   │       ├── workflow.md # 工作流程
│   │       └── prompt.md   # Sub-agent 提示词
│   ├── renwu-guanxi/
│   │   ├── SKILL.md        # 人物关系（主调度）
│   │   └── references/
│   │       ├── workflow.md
│   │       └── prompt.md
│   └── shijian-xian/
│       ├── SKILL.md        # 事件线（主调度）
│       └── references/
│           ├── workflow.md
│           └── prompt.md
│
├── tools/
│   └── novel_splitter.py   # Python 拆分工具（含占位符）
│
├── scripts/
│   ├── install.sh          # macOS/Linux 安装脚本
│   ├── install.ps1         # Windows 安装脚本
│   └── verify.py           # 验证脚本
│
├── test/
│   └── sample_novel.txt    # 测试文件
│
├── README.md               # 用户文档
├── DEPLOY.md               # 本文档（AI 文档）
└── LICENSE                 # MIT 许可证
```

### 占位符系统

所有路径使用占位符，安装时自动替换：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{CHAISHU_DIR}}` | 拆书工作目录 | `/Users/xxx/Root/Factory/拆书` |

## 安装流程

### 1. 目录创建

```bash
mkdir -p {ROOT_DIR}/Factory/拆书
mkdir -p {ROOT_DIR}/.claude/skills
```

### 2. 文件复制

```bash
# 复制 Skills
cp -r skills/* {ROOT_DIR}/.claude/skills/

# 复制 Python 工具
cp tools/novel_splitter.py {ROOT_DIR}/Factory/拆书/
```

### 3. 占位符替换

**macOS/Linux:**
```bash
find {ROOT_DIR}/.claude/skills -type f -name "*.md" \
  -exec sed -i '' 's|{{CHAISHU_DIR}}|{实际路径}|g' {} \;

sed -i '' 's|{{CHAISHU_DIR}}|{实际路径}|g' \
  {ROOT_DIR}/Factory/拆书/novel_splitter.py
```

**Windows PowerShell:**
```powershell
Get-ChildItem -Path "{ROOT_DIR}\.claude\skills" -Filter "*.md" -Recurse |
  ForEach-Object {
    (Get-Content $_.FullName) -replace '{{CHAISHU_DIR}}', '{实际路径}' |
    Set-Content $_.FullName
  }
```

### 4. 依赖安装

```bash
python3 -m pip install chardet
```

## Skills 工作原理

### 主入口：chai-shu

- **触发词**：`拆书`、`拆书分析`
- **功能**：显示菜单，调度其他 Skills
- **依赖**：无

### 结构扫描：chai-fen-sao-miao

- **触发词**：`拆分扫描`、`扫描小说结构`
- **功能**：
  1. 调用 `novel_splitter.py --scan` 扫描结构
  2. 生成 `structure.json`
  3. 询问用户拆分粒度
  4. 调用 `novel_splitter.py --split` 执行拆分
- **输出**：`Factory/拆书/{小说名}/` 目录

### 分章节概括：fen-zhang-jie-gai-kuo

- **架构**：主调度 + Sub-agent 并行
- **工作流**：
  1. 主进程读取拆分后的章节列表
  2. 每 10 章启动一个 Sub-agent
  3. Sub-agent 生成 500 字概括
  4. 主进程收集结果，写入 `config/part_summaries.yaml`
- **依赖**：需要先完成拆分

### 人物关系：renwu-guanxi

- **模式**：拟人阅读模式
- **工作流**：
  1. 读取章节文件
  2. 模拟人类阅读，提取人物关系
  3. 生成人物关系图谱
- **输出**：`config/characters.yaml`

### 事件线：shijian-xian

- **模式**：拟人确认模式
- **工作流**：
  1. 读取章节文件
  2. 识别关键事件
  3. 与用户确认事件重要性
  4. 生成事件时间线
- **输出**：`config/events.yaml`

## 故障排查

### 问题 1：Skills 不显示

**症状**：输入 `拆书` 无反应

**排查步骤**：
1. 检查 Skills 目录是否存在：
   ```bash
   ls -la {ROOT_DIR}/.claude/skills/chai-shu
   ```
2. 检查 SKILL.md 是否存在
3. 重启 AI 助手

### 问题 2：路径错误

**症状**：提示找不到文件

**排查步骤**：
1. 检查占位符是否替换：
   ```bash
   grep "{{CHAISHU_DIR}}" {ROOT_DIR}/.claude/skills/*/SKILL.md
   ```
2. 如果有输出，说明占位符未替换
3. 手动运行替换命令

### 问题 3：Python 工具报错

**症状**：`novel_splitter.py` 执行失败

**排查步骤**：
1. 检查 Python 版本：
   ```bash
   python3 --version  # 需要 3.7+
   ```
2. 检查依赖：
   ```bash
   python3 -c "import chardet; print(chardet.__version__)"
   ```
3. 检查文件编码：
   ```bash
   file -I {小说文件}
   ```

### 问题 4：Sub-agent 启动失败

**症状**：分章节概括时报错

**排查步骤**：
1. 检查 references/ 目录是否存在
2. 检查 workflow.md 和 prompt.md 是否存在
3. 检查路径占位符是否替换

## 兼容性说明

### AI 助手兼容性

| 工具 | Skills 目录 | 兼容性 | 说明 |
|------|-------------|--------|------|
| Claude Code | `.claude/skills/` | ✅ 完全兼容 | 默认支持 |
| Kimi CLI | `.kimi/skills/` 或 `.claude/skills/` | ✅ 兼容 | 支持两种路径 |
| OpenCode | `.claude/skills/` | ✅ 兼容 | 使用相同路径 |

### 平台兼容性

| 平台 | 路径分隔符 | Python 命令 | 安装脚本 |
|------|-----------|-------------|----------|
| macOS | `/` | `python3` | `install.sh` |
| Linux | `/` | `python3` | `install.sh` |
| Windows | `\` | `python` | `install.ps1` |

## 验证清单

安装完成后，使用以下清单验证：

- [ ] 所有 Skills 目录存在
- [ ] 所有 SKILL.md 文件存在
- [ ] novel_splitter.py 存在
- [ ] 占位符已全部替换
- [ ] chardet 依赖已安装
- [ ] 测试命令可以执行

**验证命令**：
```bash
python3 scripts/verify.py {ROOT_DIR}
```

## 技术细节

### novel_splitter.py 参数

```bash
# 扫描模式
python3 novel_splitter.py --scan <文件>
# 输出：structure.json

# 拆分模式
python3 novel_splitter.py --split <粒度> <文件>
# 粒度：卷/部/章/节/话/回/篇/集
# 输出：{小说名}/ 目录

# 帮助
python3 novel_splitter.py --help
```

### 章节识别正则

支持的章节格式：
- 中文数字：第一章、第二十三章
- 阿拉伯数字：第1章、第23章
- 英文：Chapter 1、Chapter 23
- 特殊格式：楔子、序章、尾声、后记

### 编码支持

自动识别以下编码：
- UTF-8
- GBK
- GB2312
- Big5

## 更新和维护

### 更新 Skills

1. 备份现有 Skills
2. 复制新版本到 skills/ 目录
3. 重新运行安装脚本

### 更新 Python 工具

1. 备份 novel_splitter.py
2. 复制新版本
3. 重新替换占位符

## 许可证

MIT License - 允许自由使用、修改和分发。

## 版本信息

- **版本**：v1.0
- **发布日期**：2026-01-28
- **兼容性**：Claude Code 2.x, Kimi CLI 1.x, OpenCode 1.x
