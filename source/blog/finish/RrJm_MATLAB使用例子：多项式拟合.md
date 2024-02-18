---
title: "MATLAB使用例子：多项式拟合"
date: "2024-02-18" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - 课程资料
  - 考试
  - 复习
summary: "MATLAB使用例子：多项式拟合"
author: "KhVeMx"
---

# MATLAB使用例子：多项式拟合
## 例子

### 定义待拟合的函数

``` matlab
% 定义函数 gamma 和 ceff
gamma = @(lambda) -(1 + lambda)/2 .* log((1 + lambda)/2) - (1 - lambda)/2 .* log((1 - lambda)/2);
ceff = @(beta) integral(@(lambda) gamma(lambda) .* (lambda./(1 - lambda.^2)) .* (sqrt(1 - beta.^2)./sqrt(lambda.^2 - beta.^2)), beta, 1);
```
这是一个看起来行为复杂的函数$c_{eff}(\beta)$，不管形式如何，写出来能求出来数值就可以。

### 生成待拟合的数据集

``` matlab
% 数据生成用于拟合
beta_values = linspace(0.1, 0.9, 10);
ceff_values = arrayfun(ceff, beta_values);
``` 
待拟合的数据集由自变量$\beta$的值和因变量$c_{eff}$的值组成。


### 函数拟合

``` matlab
% 函数近似
% 这里以二次多项式为例
p = polyfit(beta_values, ceff_values, 2);

% 拟合后的函数
f = @(beta) p(1)*beta.^2 + p(2)*beta + p(3);

ezplot(ceff,[0,1]);
hold on
ezplot(f,[0,1]);
```
