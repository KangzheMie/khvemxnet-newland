import os
import yaml
from collections import defaultdict

def read_yaml(file_path):
    """读Markdown的YAML"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('---')
        yaml_content = content[1] if len(content) > 1 else None

        if yaml_content:
            return yaml.safe_load(yaml_content)
        else:
            return None
        

# 获取脚本所在目录的绝对路径   更改当前工作目录
script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)

# 用于存储分类数据的字典
category_titles = {
    'DmZi': '电子',
    'WuLi': '物理',
    'SuXt': '数学',
    'RrJm': '软件',
    'LoGi': '逻辑',
    'SeHv': '社会',
}
categories = defaultdict(list)

# 遍历目录中的所有文件
for filename in os.listdir('./blogs'):
    if filename.endswith(".md"):
        md_yaml_data = read_yaml(f"./blogs/{filename}")
        category = md_yaml_data['categories']
        date = md_yaml_data['date']
        title = md_yaml_data['title']
        url = f"/index.html?blog={os.path.splitext(filename)[0]}"
        categories[category].append((date, title, url))

        # print(f"检测到 {filename}")
    else:
        print(f"不符合条件 检测到 {filename} ")
        

# 为每个分类生成HTML文件
for category, events in categories.items():
    filepath = f'./pages/{category}.md'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<div class="timeline">\n')
        f.write(f'    <h2>{category_titles.get(category, "通用标题")}</h2>\n')
        f.write('    <ul>\n')
        for date, title, url in sorted(events, key=lambda x: x[0], reverse=True):  # 按日期倒序排序
            f.write(f'        <li>\n')
            f.write(f'            <span class="date">{date}</span>\n')
            f.write(f'            <span class="event"><a href="{url}">{title}</a></span>\n')
            f.write('        </li>\n')
        f.write('    </ul>\n')
        f.write('</div>\n')
    print(f"{category}.md生成完毕。")