from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
import re
import yaml

# 获取当前脚本文件的完整路径
work_path = __file__

# 获取脚本文件所在的目录
work_dir = os.path.dirname(work_path)

# 改变当前工作目录到脚本文件所在目录
os.chdir(work_dir)

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    categories = Column(String)
    summary = Column(Text)
    author = Column(String)
    tags = relationship('Tag', secondary='file_tags')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class FileTag(Base):
    __tablename__ = 'file_tags'
    file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


# 创建数据库引擎
engine = create_engine('sqlite:///markdown_files.db')
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


def parse_markdown_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 尝试从文件中提取YAML头部
        try:
            # 提取YAML头部
            metadata, markdown = content.split('---', 2)[1:]
            # 解析YAML
            data = yaml.safe_load(metadata)
            return data
        except ValueError:
            # 如果没有三个分隔符或其他问题，则返回None
            return None
        
def save_to_database(data, session):
    if data:
        # 处理文件的基本信息
        file = File(
            title=data.get('title'),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d'),
            categories=data.get('categories'),
            summary=data.get('summary'),
            author=data.get('author')
        )
        session.add(file)
        session.commit()

        # 处理标签
        tags = data.get('tags', [])  # 默认为空列表，以防没有'tags'键
        for tag_name in tags:
            tag_name = tag_name.strip()  # 清除可能的前后空白
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.commit()
            file.tags.append(tag)
        session.commit()


# 遍历目录并处理每个文件
for filename in os.listdir('./md'):
    if filename.endswith('.md'):
        file_path = f'./md/{filename}'
        data = parse_markdown_file(file_path)
        save_to_database(data, session)

# for filename in os.listdir('./md'):
#     if filename.endswith('.md'):
#         file_path = f'./md/{filename}'
#         data = parse_markdown_file(file_path)
#         if data:
#             with open('./log.txt', 'a', newline='') as file:
#                 file.write(f'{data['categories']}, {data['title']}, {data['tags']}\n')