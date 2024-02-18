---
title: "MATLAB使用例子：数值积分"
date: "2024-02-18" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - 课程资料
  - 考试
  - 复习
summary: "MATLAB使用例子：数值积分"
author: "KhVeMx"
---

# MATLAB使用例子：数值积分
## 例子

``` matlab
syms x
format long

fun = sin(x^2);

% 设置一个有限的上限来近似无穷大
upper = 1000;  % 可以根据需要调整这个值

result_std = int(fun, x, 0, inf); % 精确答案
result0 = int(fun, x, 0, upper);  % 使用有限上限的积分结果

delta0 = result0 - result_std;    % 计算两个结果之间的差
```