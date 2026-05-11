#!/usr/bin/env python3

# Take clipboard and convert to rich text format (HTML) + syntax highlighting, then copy it back again.

import subprocess
from markdown import markdown
from pygments.formatters import HtmlFormatter

def get_clipboard():
    return subprocess.run(['pbpaste'], capture_output=True, text=True).stdout

def set_clipboard_html(html):
    process = subprocess.Popen(
        ['osascript', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    script = f'''
    set the clipboard to «data HTML{html.encode('utf-8').hex()}»
    '''
    process.communicate(script.encode('utf-8'))

# Get clipboard content
content = get_clipboard()

# Convert markdown to HTML with syntax highlighting
html = markdown(content, extensions=['fenced_code', 'codehilite'])

# Add pygments CSS for styling with better font
css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
font_css = '''
body, pre, code {
    font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.5;
}
pre {
    padding: 12px;
    border-radius: 4px;
}
'''
full_html = f'<style>{css}{font_css}</style>{html}'

# Copy HTML to clipboard
set_clipboard_html(full_html)
print("Formatted HTML copied to clipboard")