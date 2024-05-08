---
title: "使用Python批量重命名文件"
date: "2024-03-24" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - Python
  - 文件管理
summary: "使用脚本实现一个文件夹下文件名的重命名"
author: "KhVeMx"
---

# 使用Python批量重命名文件

## 切换目录 —— 获取脚本路径path目录dir

``` py
import os

# 获取当前脚本文件的完整路径
work_path = __file__

# 获取脚本文件所在的目录
work_dir = os.path.dirname(work_path)

# 改变当前工作目录到脚本文件所在目录
os.chdir(work_dir)
```

## 筛选文件 —— 字符的匹配
这里以一些.csv表格为例。

在某次实验中，收集到了如下的表格aCHbbbMcccMV.csv。其中abc是一些数字。

``` py
# 遍历工作目录中的所有文件
for filename in os.listdir(work_dir):
    # 检查文件名是否符合给定模式
    if filename.endswith('MV.csv') and 'CH' in filename and 'M' in filename:
```

其中`.endswith()`和`.startswith()`是两个判断字符串首尾的方法。

`in`寻找字符串是否包含指定内容的方法。

这样我们就可以得到以`'MV.csv'`开头，名字中间包含`'CH'`和`'M'`的所有文件名了。


## 解析文件 —— 正则表达式
如果想要把文件名解析得到各个组件，需要用到字符串的检测和匹配。

``` py
import re

# 正则表达式中包含三个捕获组
pattern = r'(\d+)([A-Za-z]+)(\d+)'

# 待匹配的字符串
text = "123ABC456"

# 进行匹配
match = re.match(pattern, text)

if match:
    # 使用.groups()获取所有捕获组的内容
    groups = match.groups() # .groups()方法返回一个元组
    print(groups)  # 输出: ('123', 'ABC', '456')

```

正则表达式r'(\d+)([A-Za-z]+)(\d+)'中，括号`()`定义了三个捕获组，这些捕获组指定了正则表达式匹配时需要“记住”或捕获的部分。正则表达式引擎会按照这些捕获组在表达式中出现的顺序来进行匹配，并且每个捕获组会匹配到的字符串片段。

1. **第一个捕获组** `(\d+)`：匹配一个或多个数字。`\d`代表数字字符，`+`代表一个或多个前面的元素。因此，这个组会匹配连续的数字序列，直到遇到非数字字符。
   
2. **第二个捕获组** `([A-Za-z]+)`：匹配一个或多个英文字母（不区分大小写）。`[A-Za-z]`定义了一个字符集，包括所有大写和小写字母，`+`同样表示匹配一个或多个前面的元素。这个组会从第一个组匹配结束的地方开始，继续匹配直到遇到非字母字符。

3. **第三个捕获组** `(\d+)`：这个组的匹配逻辑与第一个组相同，也是匹配一系列的数字，但它会从第二个组匹配结束的位置开始匹配。

正则表达式的匹配是按顺序进行的，从左到右。在匹配过程中，引擎会尝试按照表达式定义的模式依次匹配字符串。这意味着：

- **第一个捕获组**会首先尝试匹配字符串开始的部分，找到一系列的数字。
- 接着，**第二个捕获组**从第一个组匹配结束的地方开始，尝试匹配一系列的字母。
- 最后，**第三个捕获组**接着上一个组的匹配结束位置，匹配后续的数字。

只有当整个表达式成功匹配字符串时，`.match()`方法才会返回一个`match`对象，通过该对象的`.groups()`方法可以得到一个包含所有捕获组匹配结果的元组。**如果在任何点上匹配失败，`.match()`会立即返回`None`，表示没有找到匹配。**

这个过程不仅是逐步的，还遵循贪婪匹配原则，意味着每个捕获组会尽可能多地匹配字符，直到满足下一个模式的需要或整个模式匹配完成。

所以对于实验数据aCHbbbMcccMV.csv，可以实验如下的脚本得到各个部分的数据。

``` py
import re

# 示例字符串
filename = "7HC123M456MV.csv"

# 定义正则表达式
# 这个表达式假设“x”为数字，并且每部分至少有一个数字
pattern = r'(\d+HC)(\d+M)(\d+MV)\.csv'

# 使用正则表达式搜索
match = re.match(pattern, filename)

if match:
    # 如果匹配成功，提取各个组
    part1, part2, part3 = match.groups()
    print("Matched parts:", part1, part2, part3)
else:
    print("No match found.")
```

## 重命名文件
假设已经根据解析文件名和各种手段完成了构建新的文件名。例如

```py
# 构建新的文件名
new_filename = 'A' + filename
# 构建完整的旧文件路径和新文件路径
old_file = os.path.join(work_dir, filename)
new_file = os.path.join(work_dir, new_filename)
```

然后可以直接使用重命名的方法了
```py
# 重命名文件
os.rename(old_file, new_file)
print(f'Renamed "{filename}" to "{new_filename}"')
```






