#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拆书 Skills 安装验证脚本
版本：v1.0
"""

import os
import sys
from pathlib import Path

def check_color(text, status):
    """带颜色的输出"""
    colors = {
        'green': '\033[0;32m',
        'red': '\033[0;31m',
        'yellow': '\033[1;33m',
        'reset': '\033[0m'
    }

    if status == 'ok':
        symbol = '✓'
        color = colors['green']
    elif status == 'error':
        symbol = '✗'
        color = colors['red']
    else:
        symbol = '!'
        color = colors['yellow']

    print(f"{color}{symbol}{colors['reset']} {text}")

def main():
    print("=" * 50)
    print("  拆书 Skills 安装验证")
    print("=" * 50)
    print()

    # 获取工作区根目录
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path.cwd()

    print(f"工作区目录: {root_dir}")
    print()

    # 检查目录结构
    print("检查目录结构...")
    chaishu_dir = root_dir / "Factory" / "拆书"
    skills_dir = root_dir / ".claude" / "skills"

    if chaishu_dir.exists():
        check_color(f"拆书目录存在: {chaishu_dir}", 'ok')
    else:
        check_color(f"拆书目录不存在: {chaishu_dir}", 'error')

    if skills_dir.exists():
        check_color(f"Skills 目录存在: {skills_dir}", 'ok')
    else:
        check_color(f"Skills 目录不存在: {skills_dir}", 'error')

    print()

    # 检查 Python 工具
    print("检查 Python 工具...")
    splitter_path = chaishu_dir / "novel_splitter.py"

    if splitter_path.exists():
        check_color(f"novel_splitter.py 存在", 'ok')

        # 检查是否还有占位符
        with open(splitter_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '{{CHAISHU_DIR}}' in content:
                check_color("警告：novel_splitter.py 中仍有占位符未替换", 'warning')
            else:
                check_color("novel_splitter.py 路径配置正确", 'ok')
    else:
        check_color(f"novel_splitter.py 不存在", 'error')

    print()

    # 检查 Skills
    print("检查 Skills...")
    skills = ["chai-shu", "chai-fen-sao-miao", "fen-zhang-jie-gai-kuo", "renwu-guanxi", "shijian-xian"]
    all_ok = True

    for skill in skills:
        skill_path = skills_dir / skill / "SKILL.md"
        if skill_path.exists():
            check_color(f"{skill} 存在", 'ok')

            # 检查是否还有占位符
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '{{CHAISHU_DIR}}' in content:
                    check_color(f"  警告：{skill} 中仍有占位符未替换", 'warning')
                    all_ok = False
        else:
            check_color(f"{skill} 不存在", 'error')
            all_ok = False

    print()

    # 检查 Python 依赖
    print("检查 Python 依赖...")
    try:
        import chardet
        check_color("chardet 已安装", 'ok')
    except ImportError:
        check_color("chardet 未安装", 'error')
        all_ok = False

    print()
    print("=" * 50)

    if all_ok:
        check_color("所有检查通过！", 'ok')
        return 0
    else:
        check_color("部分检查未通过，请检查上述错误", 'warning')
        return 1

if __name__ == "__main__":
    sys.exit(main())
