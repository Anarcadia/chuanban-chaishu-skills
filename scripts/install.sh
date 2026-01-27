#!/bin/bash
# 拆书 Skills 安装脚本 (macOS/Linux)
# 版本：v1.0

set -e  # 遇到错误立即退出

echo "======================================"
echo "  拆书 Skills 安装脚本 v1.0"
echo "======================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检测 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误：未找到 Python。请先安装 Python 3.7+${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} 检测到 Python: $PYTHON_CMD"

# 检查 Python 版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "  Python 版本: $PYTHON_VERSION"
echo ""

# 询问工作区根目录
echo "请输入你的工作区根目录路径："
echo "  示例: /Users/yourname/Root"
echo "  或直接按回车使用当前目录的上级目录"
echo ""
read -p "工作区路径: " ROOT_DIR

# 如果用户没有输入，使用默认值
if [ -z "$ROOT_DIR" ]; then
    ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
    echo -e "${YELLOW}使用默认路径: $ROOT_DIR${NC}"
fi

# 验证目录存在
if [ ! -d "$ROOT_DIR" ]; then
    echo -e "${RED}错误：目录不存在: $ROOT_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} 工作区目录: $ROOT_DIR"
echo ""

# 设置拆书目录
CHAISHU_DIR="$ROOT_DIR/Factory/拆书"

# 创建必要的目录
echo "创建目录结构..."
mkdir -p "$CHAISHU_DIR"
mkdir -p "$ROOT_DIR/.claude/skills"

echo -e "${GREEN}✓${NC} 目录创建完成"
echo ""

# 复制 Skills
echo "安装 Skills..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"

cp -r "$PACKAGE_DIR/skills/"* "$ROOT_DIR/.claude/skills/"
echo -e "${GREEN}✓${NC} Skills 复制完成"
echo ""

# 复制 Python 工具
echo "安装 Python 工具..."
cp "$PACKAGE_DIR/tools/novel_splitter.py" "$CHAISHU_DIR/"
echo -e "${GREEN}✓${NC} Python 工具复制完成"
echo ""

# 替换占位符
echo "配置路径..."
find "$ROOT_DIR/.claude/skills" -type f -name "*.md" -exec sed -i '' "s|{{CHAISHU_DIR}}|$CHAISHU_DIR|g" {} \;
sed -i '' "s|{{CHAISHU_DIR}}|$CHAISHU_DIR|g" "$CHAISHU_DIR/novel_splitter.py"
echo -e "${GREEN}✓${NC} 路径配置完成"
echo ""

# 安装 Python 依赖
echo "安装 Python 依赖..."
$PYTHON_CMD -m pip install chardet --quiet
echo -e "${GREEN}✓${NC} Python 依赖安装完成"
echo ""

# 测试安装
echo "测试安装..."
if [ -f "$CHAISHU_DIR/novel_splitter.py" ]; then
    echo -e "${GREEN}✓${NC} novel_splitter.py 安装成功"
else
    echo -e "${RED}✗${NC} novel_splitter.py 安装失败"
fi

SKILLS=("chai-shu" "chai-fen-sao-miao" "fen-zhang-jie-gai-kuo" "renwu-guanxi" "shijian-xian")
for skill in "${SKILLS[@]}"; do
    if [ -d "$ROOT_DIR/.claude/skills/$skill" ]; then
        echo -e "${GREEN}✓${NC} $skill 安装成功"
    else
        echo -e "${RED}✗${NC} $skill 安装失败"
    fi
done

echo ""
echo "======================================"
echo -e "${GREEN}安装完成！${NC}"
echo "======================================"
echo ""
echo "使用方法："
echo "  1. 在 Claude Code 中输入 '拆书' 即可启动"
echo "  2. 或直接使用 Python 工具："
echo "     $PYTHON_CMD $CHAISHU_DIR/novel_splitter.py --help"
echo ""
echo "测试命令："
echo "  $PYTHON_CMD $CHAISHU_DIR/novel_splitter.py --scan <小说文件>"
echo ""
