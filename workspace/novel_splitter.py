#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说拆分工具
功能：扫描小说结构、识别章节、执行拆分
"""

import os
import re
import json
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import chardet
import unicodedata

# 拆书工作目录（默认使用脚本所在目录）
WORK_DIR = Path(__file__).parent

# ============== 章节识别正则模式 ==============

CHAPTER_PATTERNS = {
    '卷': [
        r'^第[一二三四五六七八九十百千零\d]+卷[\s:：]*(.*?)$',
        r'^卷[一二三四五六七八九十百千零\d]+[\s:：]*(.*?)$',
    ],
    '部': [
        r'^第[一二三四五六七八九十百千零\d]+部[\s:：]*(.*?)$',
    ],
    '章': [
        r'^第[一二三四五六七八九十百千零\d]+章[\s:：]*(.*?)$',
        r'^Chapter\s*\d+[\s:：]*(.*?)$',
    ],
    '节': [
        r'^第[一二三四五六七八九十百千零\d]+节[\s:：]*(.*?)$',
    ],
    '话': [
        r'^第[一二三四五六七八九十百千零\d]+话[\s:：]*(.*?)$',
    ],
    '回': [
        r'^第[一二三四五六七八九十百千零\d]+回[\s:：]*(.*?)$',
    ],
    '篇': [
        r'^第[一二三四五六七八九十百千零\d]+篇[\s:：]*(.*?)$',
    ],
    '集': [
        r'^第[一二三四五六七八九十百千零\d]+集[\s:：]*(.*?)$',
    ],
    '特殊': [
        r'^(序章|楔子|引子|前言)[\s:：]+(.*)$',
        r'^(终章|尾声|后记|完结感言)[\s:：]+(.*)$',
        r'^(番外|特别篇|番外篇)[\s:：\d]+(.*)$',
    ],
}

# 层级优先级（从高到低）
LEVEL_PRIORITY = ['卷', '部', '篇', '章', '集', '回', '话', '节', '特殊']


class NovelScanner:
    """小说结构扫描器"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.encoding = ""
        self.lines = []
        self.structure = {}  # 各层级章节统计
        self.chapters = []   # 识别到的章节列表

    def detect_encoding(self) -> str:
        """检测文件编码"""
        with open(self.file_path, 'rb') as f:
            raw = f.read(10000)  # 读取前10KB检测
            result = chardet.detect(raw)
            return result['encoding'] or 'utf-8'

    def load_file(self) -> bool:
        """加载文件内容"""
        try:
            if self.file_path.suffix.lower() == '.epub':
                return self._load_epub()
            else:
                return self._load_text()
        except Exception as e:
            print(f"错误：无法加载文件 - {e}")
            return False

    def _load_text(self) -> bool:
        """加载txt/md文件"""
        self.encoding = self.detect_encoding()
        try:
            with open(self.file_path, 'r', encoding=self.encoding, errors='ignore') as f:
                self.content = f.read()
            self.lines = self.content.split('\n')
            return True
        except Exception as e:
            # 尝试常见编码
            for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                try:
                    with open(self.file_path, 'r', encoding=enc, errors='ignore') as f:
                        self.content = f.read()
                    self.lines = self.content.split('\n')
                    self.encoding = enc
                    return True
                except:
                    continue
            return False

    def _load_epub(self) -> bool:
        """加载epub文件"""
        try:
            import zipfile
            from html.parser import HTMLParser

            class HTMLTextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []

                def handle_data(self, data):
                    self.text.append(data)

                def get_text(self):
                    return '\n'.join(self.text)

            text_parts = []
            with zipfile.ZipFile(self.file_path, 'r') as zf:
                for name in zf.namelist():
                    if name.endswith(('.html', '.xhtml', '.htm')):
                        try:
                            content = zf.read(name).decode('utf-8', errors='ignore')
                            parser = HTMLTextExtractor()
                            parser.feed(content)
                            text_parts.append(parser.get_text())
                        except:
                            continue

            self.content = '\n'.join(text_parts)
            self.lines = self.content.split('\n')
            self.encoding = 'epub'
            return True
        except Exception as e:
            print(f"错误：无法解析epub - {e}")
            return False

    def scan_structure(self) -> Dict:
        """扫描章节结构"""
        self.structure = {level: [] for level in LEVEL_PRIORITY}

        for line_num, line in enumerate(self.lines):
            line = line.strip()
            if not line:
                continue

            for level, patterns in CHAPTER_PATTERNS.items():
                for pattern in patterns:
                    match = re.match(pattern, line, re.IGNORECASE)
                    if match:
                        title = match.group(1).strip() if match.groups() else ""
                        self.structure[level].append({
                            'line_num': line_num,
                            'full_title': line,
                            'title': title,
                            'level': level
                        })
                        break

        return self.structure

    def get_summary(self) -> Dict:
        """获取结构摘要"""
        summary = {
            'file_name': self.file_path.name,
            'file_size': self.file_path.stat().st_size,
            'encoding': self.encoding,
            'total_lines': len(self.lines),
            'total_chars': len(self.content),
            'levels': {}
        }

        for level in LEVEL_PRIORITY:
            count = len(self.structure.get(level, []))
            if count > 0:
                items = self.structure[level]
                summary['levels'][level] = {
                    'count': count,
                    'first': items[0]['full_title'] if items else None,
                    'last': items[-1]['full_title'] if items else None,
                }

        return summary

    def print_report(self):
        """打印扫描报告"""
        summary = self.get_summary()

        print("\n" + "="*60)
        print("小说结构扫描报告")
        print("="*60)
        print(f"文件名：{summary['file_name']}")
        print(f"文件大小：{summary['file_size'] / 1024:.1f} KB")
        print(f"编码：{summary['encoding']}")
        print(f"总行数：{summary['total_lines']}")
        print(f"总字数：{summary['total_chars']}")
        print("-"*60)
        print("检测到的章节结构：")

        if not summary['levels']:
            print("  未检测到标准章节结构")
        else:
            for level, info in summary['levels'].items():
                print(f"  * {level}级：{info['count']} 个")
                print(f"    首：{info['first']}")
                print(f"    末：{info['last']}")

        print("="*60)
        return summary


class NovelSplitter:
    """小说拆分器"""

    def __init__(self, scanner: NovelScanner, split_level: str, output_dir: str):
        self.scanner = scanner
        self.split_level = split_level
        self.output_dir = Path(output_dir)
        self.results = []
        self.anomalies = []  # 异常/无法识别的部分

    def split(self) -> List[Dict]:
        """执行拆分"""
        # 获取该层级的所有章节
        chapters = self.scanner.structure.get(self.split_level, [])

        # 同时获取特殊章节（序章、番外等）
        special = self.scanner.structure.get('特殊', [])

        # 合并并按行号排序
        all_chapters = sorted(chapters + special, key=lambda x: x['line_num'])

        if not all_chapters:
            print(f"警告：未找到 {self.split_level} 级别的章节")
            return []

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 拆分
        lines = self.scanner.lines
        total_lines = len(lines)

        for i, chapter in enumerate(all_chapters):
            start_line = chapter['line_num']

            # 确定结束行
            if i + 1 < len(all_chapters):
                end_line = all_chapters[i + 1]['line_num']
            else:
                end_line = total_lines

            # 提取内容
            content = '\n'.join(lines[start_line:end_line])

            # 生成文件名
            num = str(i + 1).zfill(3)
            # 清理标题中的非法字符
            clean_title = re.sub(r'[\\/:*?"<>|]', '', chapter['full_title'])
            clean_title = clean_title[:50]  # 限制长度
            filename = f"{num}_{clean_title}.md"

            # 写入文件
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter['full_title']}\n\n")
                f.write(content)

            self.results.append({
                'index': i + 1,
                'filename': filename,
                'title': chapter['full_title'],
                'start_line': start_line,
                'end_line': end_line,
                'char_count': len(content)
            })

        # 检查开头是否有未归类内容
        if all_chapters and all_chapters[0]['line_num'] > 0:
            pre_content = '\n'.join(lines[0:all_chapters[0]['line_num']])
            if pre_content.strip():
                self.anomalies.append({
                    'type': '开头未归类内容',
                    'lines': f"0-{all_chapters[0]['line_num']}",
                    'char_count': len(pre_content),
                    'note': '已合并到第一章'
                })
                # 将开头内容合并到第一章
                first_file = self.output_dir / self.results[0]['filename']
                with open(first_file, 'r', encoding='utf-8') as f:
                    original = f.read()
                with open(first_file, 'w', encoding='utf-8') as f:
                    f.write(f"<!-- 以下为正文前内容 -->\n\n{pre_content}\n\n<!-- 正文开始 -->\n\n{original}")

        return self.results

    def print_report(self):
        """打印拆分报告"""
        print("\n" + "="*60)
        print("拆分完成报告")
        print("="*60)
        print(f"拆分层级：{self.split_level}")
        print(f"输出目录：{self.output_dir}")
        print(f"生成文件：{len(self.results)} 个")

        total_chars = sum(r['char_count'] for r in self.results)
        print(f"总字数：{total_chars}")

        if self.anomalies:
            print("-"*60)
            print("异常情况：")
            for a in self.anomalies:
                print(f"  * {a['type']}：{a['note']}")

        print("-"*60)
        print("章节列表：")
        for r in self.results[:10]:  # 只显示前10个
            print(f"  {r['index']:3d}. {r['title'][:40]}... ({r['char_count']}字)")
        if len(self.results) > 10:
            print(f"  ... 共 {len(self.results)} 章")

        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='小说拆分工具')
    parser.add_argument('file', help='小说文件路径 (txt/epub)')
    parser.add_argument('--scan', action='store_true', help='仅扫描结构，不拆分')
    parser.add_argument('--split', type=str, help='指定拆分层级 (卷/章/节/话等)')
    parser.add_argument('--output', type=str, help='输出目录')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')

    args = parser.parse_args()

    # 扫描
    scanner = NovelScanner(args.file)
    if not scanner.load_file():
        print("错误：无法加载文件")
        return 1

    scanner.scan_structure()

    if args.json:
        # JSON输出模式
        summary = scanner.get_summary()
        summary['structure'] = scanner.structure
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        scanner.print_report()

    # 如果指定了拆分
    if args.split:
        if args.split not in LEVEL_PRIORITY and args.split != '特殊':
            print(f"错误：不支持的拆分层级 '{args.split}'")
            print(f"支持的层级：{', '.join(LEVEL_PRIORITY)}")
            return 1

        # 确定输出目录和项目目录
        source_file = Path(args.file)
        book_name = source_file.stem

        if args.output:
            output_dir = Path(args.output)
            project_dir = output_dir.parent
        else:
            # 智能确定项目目录，避免嵌套
            parent_dir = source_file.parent
            parent_name = parent_dir.name

            # 清理书名的函数（去掉书名号，并规范化Unicode字符）
            def clean_book_name(name):
                # NFD -> NFC 规范化，处理日文浊音等组合字符
                normalized = unicodedata.normalize('NFC', name)
                # 去掉书名号
                return normalized.replace("《", "").replace("》", "").replace("「", "").replace("」", "")

            # 检查是否已在书名目录中（防止嵌套）
            if parent_dir.parent == WORK_DIR and clean_book_name(parent_name) == clean_book_name(book_name):
                # 父目录就是项目目录（在 WORK_DIR 下）
                project_dir = parent_dir

                # 检查是否存在嵌套的书名号目录，如果存在则合并
                nested_dirs = [
                    parent_dir / f"《{book_name}》",
                    parent_dir / f"{book_name}",
                    parent_dir / f"「{book_name}」"
                ]
                for nested_dir in nested_dirs:
                    if nested_dir.exists() and nested_dir != parent_dir:
                        print(f"检测到嵌套目录：{nested_dir}，将合并到父目录")
                        # 移动所有内容到父目录
                        for item in nested_dir.iterdir():
                            target = parent_dir / item.name
                            if target.exists():
                                print(f"  跳过已存在的文件：{item.name}")
                            else:
                                shutil.move(str(item), str(parent_dir))
                                print(f"  移动：{item.name}")
                        # 删除空的嵌套目录
                        try:
                            nested_dir.rmdir()
                            print(f"  已删除嵌套目录")
                        except:
                            print(f"  无法删除嵌套目录（可能非空）")
            elif clean_book_name(parent_name) == clean_book_name(book_name):
                # 父目录名匹配书名，但不在 WORK_DIR 下（可能是子目录），使用父目录
                project_dir = parent_dir
            else:
                # 不在项目目录中，创建新的项目目录（统一在 WORK_DIR 下，不带书名号）
                project_dir = WORK_DIR / clean_book_name(book_name)

            output_dir = project_dir / "拆分"

        splitter = NovelSplitter(scanner, args.split, output_dir)
        splitter.split()

        if not args.json:
            splitter.print_report()
        else:
            print(json.dumps({
                'results': splitter.results,
                'anomalies': splitter.anomalies
            }, ensure_ascii=False, indent=2))

        # 拆分完成后，移动源文件到项目目录
        target_source_path = project_dir / f"{book_name}.txt"
        if source_file.resolve() != target_source_path.resolve():
            if source_file.exists():
                # 确保项目目录存在
                project_dir.mkdir(parents=True, exist_ok=True)
                # 移动源文件
                shutil.move(str(source_file), str(target_source_path))
                print(f"\n源文件已移动至：{target_source_path}")

    return 0


if __name__ == '__main__':
    exit(main())
