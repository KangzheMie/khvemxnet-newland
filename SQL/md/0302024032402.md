---
title: "MATLAB工作区中table批量转为array"
date: "2024-03-24" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - MATLAB
  - 脚本
summary: "MATLAB工作区中table批量转为array"
author: "ChatGPT"
---

# table批量转为array

```matlab
% 获取工作区中所有变量的详细信息
varsInfo = whos;

% 遍历所有变量
for i = 1:length(varsInfo)
    % 检查变量类型是否为'table'
    if strcmp(varsInfo(i).class, 'table')
        % 获取表格变量的名称
        tableName = varsInfo(i).name;
        
        % 读取表格变量
        T = eval(tableName);
        
        % 尝试将表格转换为数组（仅当表格完全由数值组成时有效）
        try
            convertedArray = table2array(T);
            
            % 存储或覆盖变量（这里是覆盖原始表格变量，您也可以选择创建新变量）
            assignin('base', tableName, convertedArray);
        catch ME
            % 如果转换失败（例如，表格包含非数值列），输出错误信息
            fprintf('无法转换表格 "%s" 到数值矩阵: %s\n', tableName, ME.message);
        end
    end
end
```