import os
import re

def convert_html_to_markdown(img_src):
    # 直接从函数参数接收src属性的值
    return f'![{img_src.split("/")[-1]}]({img_src})'

def scan_and_convert(directory):
    # 正则表达式匹配HTML图片标签的src属性
    img_pattern = r'<img src="([^"]+)"[^>]*/>'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 使用re.sub()进行替换，lambda函数中调用convert_html_to_markdown
                new_content, num_replacements = re.subn(img_pattern, lambda x: convert_html_to_markdown(x.group(1)), content)
                
                # 如果有替换发生，则写回文件
                if num_replacements > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Converted {num_replacements} image tags in: {file_path}')
                else:
                    print(f'No image tags to convert in: {file_path}')

# 替换为你的目标目录
target_directory = '.'
scan_and_convert(target_directory)