import os
import shutil
import subprocess
import glob
import yaml
from collections import defaultdict
from pathlib import Path

def read_yaml_front_matter(file_path):
    """读取并解析Markdown文件的YAML前置块"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split('---')
        yaml_content = content[1] if len(content) > 1 else None

        if yaml_content:
            return yaml.safe_load(yaml_content)
        else:
            return None

def convert_md_to_html(source_file, output_file):
    """转换Markdown文件到HTML，文件名根据YAML头部信息生成"""
    data = read_yaml_front_matter(source_file)
    if data:
        # 根据YAML头部信息构造输出文件名
        output_file_yaml = f"{data['categories']}_{data['date']}_{data['title'].replace(' ', '-')}.html"
        output_file = os.path.join(output_file, output_file_yaml)

        # 构建Pandoc命令
        command = ['pandoc', source_file, '-o', output_file, '--katex']
        
        # 调用Pandoc进行转换
        try:
            subprocess.run(command, check=True)
            print(f"文件 {source_file} 已成功转换为 {output_file}。")
        except subprocess.CalledProcessError:
            print(f"转换文件 {source_file} 时出错。")
    else:
        print(f"文件 {source_file} 中未找到YAML前置块。")

def sync_files(src_dir, dest_dir):
    """
    同步src_dir目录下的文件到dest_dir目录。
    :param src_dir: 源目录路径
    :param dest_dir: 目标目录路径
    """
    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # 遍历源目录
    for root, dirs, files in os.walk(src_dir):
        # 计算当前遍历目录相对于源目录的相对路径
        rel_path = os.path.relpath(root, src_dir)
        # 目标目录中对应的完整路径
        dest_path = os.path.join(dest_dir, rel_path)
        
        # 确保目标目录中存在相应的目录结构
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            
            # 如果目标文件不存在或源文件较新，则复制文件
            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)
                print(f'文件 {src_file} 已同步到 {dest_file}')
    
    print("同步完成！")

def add_script_to_html(directory_path):
    # 遍历指定目录下的所有HTML文件
    for html_file in Path(directory_path).glob('*.html'):
        with open(html_file, 'r+', encoding='utf-8') as file:
            content = file.read()
            script = f"""
<script>
  if (window.location.href.indexOf('?page={html_file.stem}') === -1) {{
    window.location.href = '/index.html?page=./blog/{html_file.stem}.html';
  }}
</script>
"""
            # 检查文件是否已包含该脚本
            if script.strip() not in content:
                # 在文件内容开头添加脚本
                content = script + content
                # 移动文件指针到文件开头
                file.seek(0)
                # 写入修改后的内容
                file.write(content)
                # 截断文件，移除原始内容之后的任何内容
                file.truncate()
    print("脚本添加完成！")


# 获取脚本所在目录的绝对路径   更改当前工作目录
script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)
# 查找指定路径下所有的*.md文件
md_files = glob.glob(os.path.join('./source/blog', '*.md'))
# 遍历找到的md文件列表 并将所有文件移动到finish中
for md_file in md_files:
    convert_md_to_html(md_file, './blog')
    shutil.move(md_file, os.path.join('./source/blog/finish', os.path.basename(md_file)))
# 同步md所需要的依赖文件到html工程中
sync_files('./source/blog/picture/blog', './picture/blog')

# 用于存储分类数据的字典
categories = defaultdict(list)
category_titles = {
    'DmZi': '电子',
    'WuLi': '物理',
    'SuXt': '数学',
    'RrJm': '软件',
    'LoGi': '逻辑',
    'SeHv': '社会',
}

# 遍历目录中的所有文件
for filename in os.listdir('./blog'):
    if filename.endswith(".html"):
        parts = filename.split('_')
        if len(parts) == 3:
            category, date, title_with_extension = parts
            title = title_with_extension.split('.')[0]
            url = f'./blog/{filename}'
            # 将信息添加到对应的分类中
            categories[category].append((date, title, url))

# 为每个分类生成HTML文件
for category, events in categories.items():
    filepath = f'./blog/blog_{category}.html'
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
    print(f"blog_{category}.html生成完毕。")

add_script_to_html('./blog')
