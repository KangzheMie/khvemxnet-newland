import os
import yaml

# 获取当前脚本文件的完整路径
work_path = __file__

# 获取脚本文件所在的目录
work_dir = os.path.dirname(work_path)

# 改变当前工作目录到脚本文件所在目录
os.chdir(work_dir)

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

markdown_folder_path = './md'

categories_code = {
    'DmZi': '010',
    'LoGi': '020',   
    'RrJm': '030',   
    'WuLi': '040',   
    'SuXt': '050',   
    'SeHv': '060',   
}

markdown_files = os.listdir(markdown_folder_path)

for markdown_filename in markdown_files:
    #如果是md文件
    if markdown_filename.endswith('.md'):
        markdown_file_path = f'{markdown_folder_path}/{markdown_filename}'
        markdown_file_data = parse_markdown_file(markdown_file_path)
        # 如果文件信息存在
        if markdown_file_data:
            categories = markdown_file_data['categories']
            # 如果文件类别合法
            if categories in categories_code:
                markdown_file_newname_repeatNum = 0
                markdown_file_newname = f'{categories_code[categories]}{markdown_file_data['date'].replace('-','')}{markdown_file_newname_repeatNum:02}.md'
                # 检查在当前文件中有无重名，有重名就+1，直到没有重名
                while markdown_file_newname in os.listdir(markdown_folder_path):
                    markdown_file_newname_repeatNum += 1
                    markdown_file_newname = f'{categories_code[categories]}{markdown_file_data['date'].replace('-','')}{markdown_file_newname_repeatNum:02}.md'

                # 构建完整的旧文件路径和新文件路径
                old_file = os.path.join(markdown_folder_path, markdown_filename)
                new_file = os.path.join(markdown_folder_path, markdown_file_newname)

                # 重命名文件
                os.rename(old_file, new_file)
                #print(f'Renamed "{filename}" to "{markdown_file_newname}"')
            else:
                print('error, category has not been found')
            
        
