import os
import re
import yaml
from collections import defaultdict
import sqlite3

# 获取脚本所在目录的绝对路径   更改当前工作目录
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# 获取文件夹中所有文件名
folderPath = "./blogs"
file_list = os.listdir(folderPath)
file_list.remove('.gitkeep')

# ========================== 函数区 ========================== #

# 从文件中提取YAML头部
def markdown_yaml(folderPath, fileName):
    filePath = folderPath + '/' + fileName
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
        
        try:
            metadata = content.split('---', 2)[1]
            data = yaml.safe_load(metadata)
            return (fileName, data['title'], data['date'], data['categories'], data['summary'], data['author'])
        
        except ValueError:
            return None
        
# 从文件中提取YAML头部中的标签信息
def markdown_yaml_tag(folderPath, fileName):
    filePath = folderPath + '/' + fileName
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
        
        try:
            metadata = content.split('---', 2)[1]
            data = yaml.safe_load(metadata)
            return (data['tags'], data['title'], fileName)
        
        except ValueError:
            return None
        
# 从文件中提取图片的引用信息
def markdown_text_picture(folderPath, fileName):
    filePath = folderPath + '/' + fileName
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
        
        try:
            text = content.split('---', 2)[2]
            matches = re.findall(r'^\s*!\[(.*?)\]\((.*?)\)\s*$', text, re.MULTILINE)
            return (fileName, matches)
        
        except ValueError:
            return None
        

# ========================== 数据库区 ========================== #

# 连接到SQLite数据库
conn = sqlite3.connect('blogs.db')
cursor = conn.cursor()

# 将博客文件记录在表格中
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MarkdownFiles';")
table_exists = cursor.fetchone()
# 如果表不存在，则创建表
if not table_exists:
    cursor.execute('''CREATE TABLE MarkdownFiles (
id INTEGER PRIMARY KEY AUTOINCREMENT,
FileName TEXT NOT NULL,
Title TEXT NOT NULL,
Date TEXT NOT NULL,
Categories TEXT NOT NULL,
Summary TEXT,
Author TEXT NOT NULL
);''')

# 获取SQLite表中的所有文件名并同步
cursor.execute("SELECT FileName FROM MarkdownFiles")
sqlite_file_list = [row[0] for row in cursor.fetchall()]

files_to_add    = set(file_list) - set(sqlite_file_list)
for file in files_to_add:
    cursor.execute('''
    INSERT INTO MarkdownFiles (FileName, Title, Date, Categories, Summary, Author)
    VALUES (?, ?, ?, ?, ?, ?)
''', markdown_yaml(folderPath, file))

files_to_delete = set(sqlite_file_list) - set(file_list)
for file in files_to_delete:
    cursor.execute("DELETE FROM MarkdownFiles WHERE FileName = ?", (file,))


# 提交更改
conn.commit()

# 将博客标签记录在表格中
cursor.execute('DROP TABLE IF EXISTS MarkdownTag;')
cursor.execute('''CREATE TABLE MarkdownTag (
Tags TEXT NOT NULL,
Title TEXT NOT NULL,
FileName TEXT NOT NULL
);''')

# 填充 Tags 表
for file in file_list:
    data = markdown_yaml_tag(folderPath, file)
    tags  = data[0]
    title = data[1]
    filename = data[2]
    # 插入每个标签和标题的组合
    for tag in tags:
        cursor.execute('''
            INSERT INTO MarkdownTag (Tags, Title, FileName)
            VALUES (?, ?, ?)
        ''', (tag, title, filename))

# 提交更改
conn.commit()

# 计算标签出现次数
cursor.execute('DROP TABLE IF EXISTS MarkdownTagCount')
cursor.execute('''
CREATE TABLE MarkdownTagCount (
    Tags TEXT NOT NULL,
    Count INTEGER NOT NULL
)
''')

cursor.execute('''
SELECT Tags, COUNT(*)
FROM MarkdownTag
GROUP BY Tags
''')
results = cursor.fetchall()

cursor.executemany('INSERT INTO MarkdownTagCount (Tags, Count) VALUES (?, ?)', results)

# 提交更改
conn.commit()

# 处理图片信息
cursor.execute('DROP TABLE IF EXISTS MarkdownPicture;')
cursor.execute('''CREATE TABLE MarkdownPicture (
FileName TEXT NOT NULL,
Alt TEXT,
Src TEXT NOT NULL
);''')

# 填充 Picture 表
for file in file_list:
    data = markdown_text_picture(folderPath, file)
    filename = data[0]
    pictures = data[1]
    # 插入每个标签和标题的组合
    for picture in pictures:
        cursor.execute('''
            INSERT INTO MarkdownPicture (FileName, Alt, Src)
            VALUES (?, ?, ?)
        ''', (filename, picture[0], picture[1]))


# 提交更改并关闭连接
conn.commit()
conn.close()

# ========================== 网页生成区 ========================== #

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

# 将目录中的文件存储进 category : (date, title, url) 的键值对中
for fileName in file_list:
    if fileName.endswith(".md"):
        data        = markdown_yaml(folderPath, fileName)
        title       = data[1]
        date        = data[2]
        category    = data[3]
        url         = f"/index.html?blog={os.path.splitext(fileName)[0]}"

        categories[category].append((date, title, url))
    else:
        print(f"{fileName} 不符合条件")
        
# 根据字典生成索引页面
for category, events in categories.items():
    # 每一个分类下面是若干的事件
    # 事件由 [(日期, 标题, url) ... ...] 组成

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