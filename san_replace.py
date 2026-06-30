#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量替换《故事会》项目文件中 SAN/San/san → 理智
只替换游戏术语，不误伤英文单词
"""

import os
import re

# 项目根目录
ROOT = r"C:\Users\80526\WorkBuddy\2026-06-05-15-49-56"

# 需要跳过的目录/文件
SKIP_DIRS = {'.git', '__pycache__', 'node_modules'}
SKIP_FILES = set()  # 可以在这里加跳过文件

# 需要处理的文件扩展名
EXTENSIONS = {'.md'}

def replace_san_in_file(filepath):
    """对单个文件做SAN→理智替换，返回变更行数"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, FileNotFoundError):
        return 0

    original = content

    # 替换顺序很重要：先替换带后缀的，再替换单独的
    
    # 1. SAN值/San值/san值 → 理智值
    content = re.sub(r'\bSAN(?=/)', '理智', content)
    content = re.sub(r'\bSan(?=/)', '理智', content)
    content = re.sub(r'\bsan(?=/)', '理智', content)
    
    # 2. SAN-1/San-1/san-1 等数值格式 → 理智-1
    content = re.sub(r'\bSAN(\s*[-+]\s*\d)', r'理智\1', content)
    content = re.sub(r'\bSan(\s*[-+]\s*\d)', r'理智\1', content)
    content = re.sub(r'\bsan(\s*[-+]\s*\d)', r'理智\1', content)
    
    # 3. SAN值/San值/san值 → 理智值
    content = re.sub(r'\bSAN值\b', '理智值', content)
    content = re.sub(r'\bSan值\b', '理智值', content)
    content = re.sub(r'\bsan值\b', '理智值', content)
    
    # 4. 单独的SAN/San/san（前后有空格、标点、行首行尾）
    # 先处理带标点符号的情况
    content = re.sub(r'\bSAN\b', '理智', content)
    content = re.sub(r'\bSan\b', '理智', content)
    # 小写san需要小心，只在明显是游戏术语的上下文替换
    # 先替换 san- 和 san+
    content = re.sub(r'(?<![a-zA-Z])(?<![\w])san(?=[-+])', '理智', content)
    # 替换 "san值"
    content = re.sub(r'(?<![a-zA-Z])(?<![\w])san(?=值)', '理智', content)
    # 替换单独的 san（前后有空格或标点）
    content = re.sub(r'(?<![a-zA-Z])(?<![\w])san(?=[^a-zA-Z]|$)', '理智', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0


def main():
    changed = []
    skipped = []
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 跳过指定目录
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in EXTENSIONS:
                continue
            fullpath = os.path.join(dirpath, fn)
            if fn in SKIP_FILES:
                skipped.append(fullpath)
                continue
            
            result = replace_san_in_file(fullpath)
            if result:
                changed.append(fullpath[len(ROOT)+1:])
    
    print(f"✅ 已处理 {len(changed)} 个文件")
    if changed:
        print("\n变更文件清单：")
        for f in changed:
            print(f"  - {f}")
    if skipped:
        print(f"\n⏭️  跳过 {len(skipped)} 个文件")

if __name__ == '__main__':
    main()
