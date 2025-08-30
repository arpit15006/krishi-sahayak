#!/usr/bin/env python3
import os
import re

def fix_template_urls(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Replace main.* with direct route names
                content = re.sub(r"url_for\('main\.(\w+)'", r"url_for('\1'", content)
                
                with open(filepath, 'w') as f:
                    f.write(content)
                
                print(f"Fixed URLs in {filepath}")

if __name__ == '__main__':
    fix_template_urls('templates')
    print("All template URLs fixed!")