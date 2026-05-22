#!/usr/bin/env python3
"""
将 index.html 及所有依赖打包为单个独立 HTML 文件。
用法：python build.py
输出：QQ记录整理log工具.html
"""
import re
import os
import base64

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, 'index.html')
OUT  = os.path.join(BASE, 'QQ记录整理log工具.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

def read_text(rel_path):
    path = os.path.join(BASE, rel_path.replace('/', os.sep))
    if not os.path.exists(path):
        print(f'  [WARN] 找不到文件：{rel_path}')
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_binary_b64(rel_path):
    path = os.path.join(BASE, rel_path.replace('/', os.sep))
    if not os.path.exists(path):
        print(f'  [WARN] 找不到文件：{rel_path}')
        return None
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

# 内联 <script src=PATH></script>
def inline_script(m):
    src = m.group(1)
    content = read_text(src)
    if content is None:
        return m.group(0)
    print(f'  内联 JS：{src}')
    return '<script>' + content + '</script>'

html = re.sub(r'<script src=([^\s>]+)></script>', inline_script, html)

# 内联 <link href=PATH rel=stylesheet>
def inline_css(m):
    href = m.group(1)
    content = read_text(href)
    if content is None:
        return m.group(0)
    print(f'  内联 CSS：{href}')
    return '<style>' + content + '</style>'

html = re.sub(r'<link href=([^\s>]+) rel=stylesheet>', inline_css, html)

# 将 favicon 转为 base64 data URL
b64 = read_binary_b64('favicon.ico')
if b64:
    print('  内联 favicon')
    html = html.replace(
        '<link href=favicon.ico rel="shortcut icon">',
        f'<link href="data:image/x-icon;base64,{b64}" rel="shortcut icon">'
    )

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(OUT) // 1024
print(f'\n完成！输出文件：{OUT}  ({size_kb} KB)')
