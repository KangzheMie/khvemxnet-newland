---
title: "MATLAB批量导入csv"
date: "2024-03-24" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - MATLAB
  - 脚本
summary: "MATLAB批量导入csv"
author: "ChatGPT"
---

# MATLAB导入csv

## 指定目录并遍历

```matlab
% 指定文件夹路径
folderPath = './raw';
files = dir(fullfile(folderPath, '*.csv'));

% 遍历文件夹中的每个CSV文件
for i = 1:length(files)
    % 获取文件的完整路径
    fullPath = fullfile(folderPath, files(i).name);
```

## 根据文件名解析需要读出的数据
```matlab
    % 解析文件名以获取所需的列号
    % 假设列号位于文件名的第2个字符，如'A2HC001M300MV.csv'中的'2'
    columnName = files(i).name(2);
    
    % 将列号字符转换为数值类型
    columnIndex = str2double(columnName) + 3;
    
    % 使用opts对象指定输入的模式
    opts = detectImportOptions(fullPath, 'VariableNamingRule', 'preserve');
    opts.SelectedVariableNames = opts.VariableNames(columnIndex); % 选择指定列

    
    data = readmatrix(fullPath, opts);
```

这段代码中的 `opts` 实际上是一个 `import options` 对象，它在 MATLAB 中用于定义和存储导入数据时的选项设置。

### detectImportOptions函数

`detectImportOptions` 函数用于创建一个包含导入数据**所需选项**的对象。

这个函数会自动检测数据源（例如CSV文件）的格式和结构，并据此设置导入选项，以便后续的 `readtable`、`readmatrix` 或类似函数**能够按照这些选项正确读取**数据。

```matlab
opts = detectImportOptions(fullPath, 'VariableNamingRule', 'preserve');
```

在这里，`fullPath` 是数据文件的路径。

`'VariableNamingRule'`, `'preserve'` 参数指示在创建变量名时保持原始列标题的文字，而不是将非字母数字字符转换为下划线（这是 MATLAB 默认的行为）。这样，如果原始数据中的列标题包含特殊字符，这些特殊字符会被保留下来。

### opts.SelectedVariableNames属性

opts.SelectedVariableNames属性允许您**指定**在导入数据时希望读取的特定列。这对于只处理文件中某几列数据的情况非常有用，可以提高效率并减少内存使用。

```matlab
opts.SelectedVariableNames = opts.VariableNames(columnIndex);
```

这行代码设置了 `opts.SelectedVariableNames` 属性，使其只包含 `opts.VariableNames(columnIndex)` 指定的那些列。这里，`columnIndex` 是一个索引数组，指定了希望从数据源中导入哪些列。通过这种方式，可以只导入感兴趣的数据列，而不是整个数据集。

## 将读出数据data写入矩阵中
``` matlab
    data = readmatrix(fullPath, opts);

    % 将数据存储到以文件名命名的变量中
    % [路径,名字,后缀] = fileparts(filename)
    [~, fileName, ~] = fileparts(files(i).name);
    
    % 注意：MATLAB变量名不能包含特殊字符，如数字和点，因此需要对文件名进行处理
    % 以下代码将非字母字符替换为下划线，并去掉扩展名
    variableName = regexprep(fileName, '\W|^\d|\..*$', '_');

    % 将字符串输出到命令台
    eval([variableName ' = data;']);
end
```

## csv文件和xls文件的区别
CSV文件（Comma-Separated Values，逗号分隔值文件）和Excel文件（如XLS或XLSX格式）是两种常见的数据存储格式，它们在结构、功能和使用场景上有显著的区别。

### CSV文件

``` c
0,0,0,2045,487,76
1,1,0,2045,487,76
2,2,0,2045,487,76
3,3,0,2045,487,76
4,4,0,2045,487,76
```

- **结构简单**：CSV文件由纯文本组成，使用逗号（或其他分隔符，如制表符）来分隔数据中的每个字段。每行代表一条记录，类似于数据库中的一行。
- **可读性**：CSV文件可以使用任何文本编辑器打开，内容易于人类阅读和编辑。
- **兼容性**：几乎所有的编程语言、数据库和电子表格软件都支持CSV格式，使其成为数据交换的通用格式。
- **限制**：CSV格式缺乏标准化，不同的系统可能使用不同的字符作为字段分隔符。它不支持数据类型定义、多个工作表或富文本格式等复杂功能。

### Excel文件

- **功能丰富**：Excel文件格式（如XLS或XLSX）支持高级功能，包括单元格格式设置、公式、图表、图像、宏等。
- **可视化和分析工具**：Excel软件提供了强大的数据分析和可视化工具，使得处理复杂的数据集成为可能。
- **兼容性**：尽管Excel文件格式主要与Microsoft Office软件兼容，但许多其他电子表格软件也能够读取和编辑这种格式的文件。
- **文件大小和性能**：由于额外的功能和格式信息，Excel文件通常比CSV文件大，特别是在处理大量数据时可能会导致性能下降。

### 存储优势

- **CSV**的优势在于其简单性和兼容性，适合于快速交换和存储大量的纯数据。
- **Excel**的优势在于其功能的丰富性，适合于需要复杂数据分析、格式化显示和报告生成的场景。

### 将CSV视作TXT文件

CSV文件实质上是一种特定格式的文本文件，因此可以将其视为TXT文件。实际上，您可以使用文本编辑器（如Notepad）打开CSV文件，也可以将TXT文件重命名为CSV（如果内容符合CSV格式）。然而，将文件视为CSV意味着您认为文件中的数据是以逗号（或其他分隔符）分隔的，适用于表示表格数据。

总之，CSV和Excel文件各有优势，选择哪种格式取决于您的具体需求，如数据的复杂性、是否需要格式化或公式支持、以及与其他系统的兼容性需求。
