# 拆书 Skills 安装脚本 (Windows PowerShell)
# 版本：v1.0

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  拆书 Skills 安装脚本 v1.0" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检测 Python 命令
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "错误：未找到 Python。请先安装 Python 3.7+" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 检测到 Python: $pythonCmd" -ForegroundColor Green

# 检查 Python 版本
$pythonVersion = & $pythonCmd --version 2>&1
Write-Host "  Python 版本: $pythonVersion"
Write-Host ""

# 询问工作区根目录
Write-Host "请输入你的工作区根目录路径："
Write-Host "  示例: C:\Users\yourname\Root"
Write-Host "  或直接按回车使用当前目录的上级目录"
Write-Host ""
$rootDir = Read-Host "工作区路径"

# 如果用户没有输入，使用默认值
if ([string]::IsNullOrWhiteSpace($rootDir)) {
    $rootDir = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
    Write-Host "使用默认路径: $rootDir" -ForegroundColor Yellow
}

# 验证目录存在
if (-not (Test-Path $rootDir)) {
    Write-Host "错误：目录不存在: $rootDir" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 工作区目录: $rootDir" -ForegroundColor Green
Write-Host ""

# 设置拆书目录
$chaishuDir = Join-Path $rootDir "Factory\拆书"

# 创建必要的目录
Write-Host "创建目录结构..."
New-Item -ItemType Directory -Force -Path $chaishuDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $rootDir ".claude\skills") | Out-Null

Write-Host "✓ 目录创建完成" -ForegroundColor Green
Write-Host ""

# 复制 Skills
Write-Host "安装 Skills..."
$packageDir = Split-Path -Parent $PSScriptRoot
$skillsSource = Join-Path $packageDir "skills"
$skillsTarget = Join-Path $rootDir ".claude\skills"

Get-ChildItem -Path $skillsSource -Directory | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $skillsTarget -Recurse -Force
}

Write-Host "✓ Skills 复制完成" -ForegroundColor Green
Write-Host ""

# 复制 Python 工具
Write-Host "安装 Python 工具..."
$toolSource = Join-Path $packageDir "tools\novel_splitter.py"
Copy-Item -Path $toolSource -Destination $chaishuDir -Force

Write-Host "✓ Python 工具复制完成" -ForegroundColor Green
Write-Host ""

# 替换占位符
Write-Host "配置路径..."
$chaishuDirEscaped = $chaishuDir -replace '\\', '\\'
Get-ChildItem -Path (Join-Path $rootDir ".claude\skills") -Filter "*.md" -Recurse | ForEach-Object {
    (Get-Content $_.FullName) -replace '\{\{CHAISHU_DIR\}\}', $chaishuDir | Set-Content $_.FullName
}

$splitterPath = Join-Path $chaishuDir "novel_splitter.py"
(Get-Content $splitterPath) -replace '\{\{CHAISHU_DIR\}\}', $chaishuDir | Set-Content $splitterPath

Write-Host "✓ 路径配置完成" -ForegroundColor Green
Write-Host ""

# 安装 Python 依赖
Write-Host "安装 Python 依赖..."
& $pythonCmd -m pip install chardet --quiet

Write-Host "✓ Python 依赖安装完成" -ForegroundColor Green
Write-Host ""

# 测试安装
Write-Host "测试安装..."
if (Test-Path (Join-Path $chaishuDir "novel_splitter.py")) {
    Write-Host "✓ novel_splitter.py 安装成功" -ForegroundColor Green
} else {
    Write-Host "✗ novel_splitter.py 安装失败" -ForegroundColor Red
}

$skills = @("chai-shu", "chai-fen-sao-miao", "fen-zhang-jie-gai-kuo", "renwu-guanxi", "shijian-xian")
foreach ($skill in $skills) {
    if (Test-Path (Join-Path $rootDir ".claude\skills\$skill")) {
        Write-Host "✓ $skill 安装成功" -ForegroundColor Green
    } else {
        Write-Host "✗ $skill 安装失败" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法："
Write-Host "  1. 在 Claude Code 中输入 '拆书' 即可启动"
Write-Host "  2. 或直接使用 Python 工具："
Write-Host "     $pythonCmd $chaishuDir\novel_splitter.py --help"
Write-Host ""
Write-Host "测试命令："
Write-Host "  $pythonCmd $chaishuDir\novel_splitter.py --scan <小说文件>"
Write-Host ""
