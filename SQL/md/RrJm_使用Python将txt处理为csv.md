---
title: "使用Python将txt处理为csv"
date: "2024-04-15" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - Python
  - 文件管理
summary: "使用脚本实现txt处理为csv"
author: "ChatGPT"
---

# 使用Python将txt处理为csv
``` python
import argparse
import csv
import re

def main(txtfile, csvfile):
    pattern = r'(T2_1:)(-?\d+\.\d+)(T2_2:)(-?\d+\.\d+)'

    with open(csvfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['T2_1', 'T2_2'])  # 写入标题

        with open(txtfile, 'r', encoding='utf-8') as file:
            # 逐行读取和处理
            for line in file:
                match = re.search(pattern, line.strip()) # 使用strip()去除可能的空白字符
                if match:
                    # 如果匹配成功，提取各个组
                    Temperature_1 = match.group(2)
                    Temperature_2 = match.group(4)
                    writer.writerow([Temperature_1, Temperature_2])
                else:
                    print("No match found.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract temperatures from text and write to CSV.")
    parser.add_argument("txtfile", type=str, help="The path to the text file to process.")
    parser.add_argument("csvfile", type=str, help="The path to the CSV file to write.")
    
    args = parser.parse_args()

    main(args.txtfile, args.csvfile)
```

## 逐行处理txt

```python
# 打开文件
with open('example.txt', 'r', encoding='utf-8') as file:
    # 逐行读取和处理
    for line in file:
        # 这里可以添加您需要的处理逻辑
        print(line.strip())  # 使用strip()去除可能的空白字符
```

使用 `with` 语句可以确保文件在操作完成后会被正确关闭。

### 文件对象作为迭代器

当打开一个文件时，Python 创建一个文件对象，这个对象本身就是一个迭代器。迭代器是一种支持迭代（即一次返回一个元素，直到没有更多元素时停止）的对象。在Python中，文件对象的迭代是按行进行的。

**每次迭代返回文件的下一行。**

当在 `for` 循环中使用文件对象时，Python调用文件对象的 `__next__()` 方法来获取文件中的下一行。如果到达文件末尾，文件对象会自动抛出一个 `StopIteration` 异常，这告诉 `for` 循环停止迭代。


## 正则匹配

```python
import re

pattern = r'(T2_1:)(-?\d+\.\d+)'

with open('test.txt', 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())  # 打印原始行数据
        match = re.search(pattern, line.strip())  # 在整行中搜索模式
        if match:
            print("找到匹配:", match.group(0))  # 打印匹配的内容
        else:
            print("未找到匹配")
```

使用 `re.match()` 函数，该函数只在字符串开始处进行匹配检查。如果在**行的开始处没有**立即找到符合模式的内容，`re.match()` 就会返回 `None`。

**如果目标字符串可能在行内任何位置**，应使用 `re.search()` 来代替 `re.match()`。`re.search()` 会检查整个字符串，并返回第一个符合模式的匹配项。


## 提取匹配

在Python中使用正则表达式的 `match` 或 `search` 结果时，可以通过 `group()` 方法访问各个组。`group(0)` 返回整个匹配的字符串，而 `group(n)` 返回第 `n` 个括号组的匹配字符串。

假设有一个正则表达式，其中包含四个组，如下：

```python
pattern = r'(T2_1:)(-?\d+\.\d+)(T2_3:)(-?\d+\.\d+)'
```

这里，`part1` 对应于第一个括号 `(T2_1:)`，`part2` 对应于第二个括号 `(-?\d+\.\d+)`，依此类推。

```python
import re

pattern = r'(T2_1:)(-?\d+\.\d+)(T2_3:)(-?\d+\.\d+)'
text = "T2_1:28.6558T2_3:-200.0000"

match = re.search(pattern, text)
if match:
    part2 = match.group(2)  # 提取第二个组
    part4 = match.group(4)  # 提取第四个组
    print("Part2:", part2, "Part4:", part4)
else:
    print("未找到匹配")
```

## 写入csv
``` python
import csv

# 打开CSV文件准备写入
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Temperature_1', 'Temperature_2'])  # 写入标题
```

- 使用`newline=''`来防止在写入文件时出现空行。
- 确保文件路径和文件名是正确的，并且您的运行环境有权限写入文件。


## 使用命令行运行程序

要让脚本接受命令行参数，可以使用 Python 的 `argparse` 库来简单地处理命令行输入。

```python
import argparse

...

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract temperatures from text and write to CSV.")
    parser.add_argument("txtfile", type=str, help="The path to the text file to process.")
    parser.add_argument("csvfile", type=str, help="The path to the CSV file to write.")
    
    args = parser.parse_args()

    main(args.txtfile, args.csvfile)
```

使用方法
``` bash
python xxx.py test.txt output.csv
```

使用提示
```bash
PS D:\> python TempToCSV.py -h
usage: TempToCSV.py [-h] txtfile csvfile

Extract temperatures from text and write to CSV.

positional arguments:
  txtfile     The path to the text file to process.
  csvfile     The path to the CSV file to write.

options:
  -h, --help  show this help message and exit
```