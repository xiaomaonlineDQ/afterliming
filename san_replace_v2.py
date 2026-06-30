#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确替换《故事会》项目文件中 SAN/San/san → 理智
第二版：处理所有组合
"""

import os
import re

ROOT = r"C:\Users\80526\WorkBuddy\2026-06-05-15-49-56"

SKIP_DIRS = {'.git', '__pycache__', 'node_modules'}

def replace_san_v2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 按优先级排序：先替换带后缀的，再替换单独的
    
    # 1. XXX值 → 理智值
    for old, new in [('San值', '理智值'), ('SAN值', '理智值'), ('san值', '理智值')]:
        content = content.replace(old, new)
    
    # 2. XXX-数字 → 理智-数字
    content = re.sub(r'San(\s*[-+]\s*\d)', r'理智\1', content)
    content = re.sub(r'SAN(\s*[-+]\s*\d)', r'理智\1', content)
    content = re.sub(r'san(\s*[-+]\s*\d)', r'理智\1', content)
    
    # 3. XXX+数字 → 理智+数字 (同上，已包含在2里)
    
    # 4. XXX/ → 理智/
    content = content.replace('San/', '理智/').replace('SAN/', '理智/').replace('san/', '理智/')
    
    # 5. 单独的San/SAN/san（前后有空格、标点、行首行尾）
    # 处理大写SAN
    content = re.sub(r'(^|[\s\(\（\[【「])(SAN)(?=[\s\)\）\]】」,，。；;:\.!！\?？]|$)', r'\1理智', content)
    # 处理首字母大写San
    content = re.sub(r'(^|[\s\(\（\[【「])(San)(?=[\s\)\）\]】」,，。；;:\.!！\?？]|$)', r'\1理智', content)
    # 处理小写san（更保守，只在明显上下文替换）
    # 先替换 san 后面跟中文或标点的
    content = re.sub(r'(?<=[\s\(\（\[【「])san(?=[\s\)\）\]】」,，。；;:\.!！\?？]|$)', '理智', content)
    # 行首的san
    content = re.sub(r'^(san)(?=[\s\)\）\]】」,，。；;:\.!！\?？]|$)', '理智', content, flags=re.MULTILINE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            fullpath = os.path.join(dirpath, fn)
            try:
                if replace_san_v2(fullpath):
                    changed.append(fullpath[len(ROOT)+1:])
            except Exception as e:
                print(f"❌ 错误: {fullpath}: {e}")
    
    print(f"✅ 第二遍处理完成，{len(changed)} 个文件有进一步变更")
    if changed:
        print("变更文件：")
        for f in changed[:10]:
            print(f"  {f}")

if __name__ == '__main__':
    main()
