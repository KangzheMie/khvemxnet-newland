from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import os
import re
import yaml

# 获取当前脚本文件的完整路径
work_path = __file__

# 获取脚本文件所在的目录
work_dir = os.path.dirname(work_path)

# 改变当前工作目录到脚本文件所在目录
os.chdir(work_dir)

# Base = declarative_base()

# class File(Base):
#     __tablename__ = 'files'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     date = Column(Date)
#     categories = Column(String)
#     summary = Column(Text)
#     author = Column(String)
#     tags = relationship('Tag', secondary='file_tags')

# class Tag(Base):
#     __tablename__ = 'tags'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)

# class FileTag(Base):
#     __tablename__ = 'file_tags'
#     file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
#     tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


# # 创建数据库引擎
# engine = create_engine('sqlite:///markdown_files.db')
# Base.metadata.create_all(engine)

# # 创建会话
# Session = sessionmaker(bind=engine)
# session = Session()


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
        

for filename in os.listdir('./md'):
    if filename.endswith('.md'):
        file_path = f'./md/{filename}'
        data = parse_markdown_file(file_path)
        if data:
            #print(data)  # 或其他逻辑处理
            with open('./log.txt', 'a', newline='') as file:
                if 'AI' in data['tags']:
                    file.write(f'\n{data['title']}, {data['tags']}')