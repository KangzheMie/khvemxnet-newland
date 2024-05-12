---
title: "MATLAB使用例子：周期边界和取模运算"
date: "2024-02-18" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - 课程资料
  - 考试
  - 复习
summary: "MATLAB使用例子：周期边界和取模运算"
author: "KhVeMx"
---

# MATLAB使用例子：周期边界和取模运算
## 例子

``` matlab
>> mod(A-2,5) +1    % 求周期边界条件下的上一个点的姿势

ans =

     5     1     2     3     4

>> mod(A,5) + 1     % 求周期边界条件下的下一个点的姿势

ans =

     2     3     4     5     1
```