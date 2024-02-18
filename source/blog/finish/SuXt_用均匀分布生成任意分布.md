---
title: "用均匀分布生成任意分布"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: SuXt
tags:
  - 课程资料
  - 考试
  - 复习
summary: "用均匀分布生成任意分布"
author: "KhVeMx"
---

# 用均匀分布生成任意分布

## 使用均匀分布生成高斯分布

### Box-Muller方法

需要两个服从均匀分布的随机变量，然后联合生成两组服从高斯分布的数据。
$$
\begin{cases}
    y_1 = \sqrt{-2\sigma^2 \ln(1-x_1)} \sin(2\pi x_2)\\
    y_2 = \sqrt{-2\sigma^2 \ln(1-x_1)} \cos(2\pi x_2)
\end{cases}
$$

```matlab
% 生成两组均匀分布的数组
X1 = rand(100000,1);
X2 = rand(100000,1);

% 用这两组相互独立的均匀分布数组生成高斯分布
sigma = 5;
Y1 = sigma.*sqrt(-2.*log(X1)) .* sin(2.*pi.*X2);
Y2 = sigma.*sqrt(-2.*log(X1)) .* cos(2.*pi.*X2);
```


## 使用均匀分布生成指数分布
### 逆变换法

$$
    F(y) = \int_{-\infty}^{y} f(y) \mathrm{d}y
    = \int_{0}^{x} \mathrm{d}x 
    = x
$$
$$
    y = F^{-1}(x)
$$

实际上是使用了这样的一种思路：对于样本X和样本Y，那么只要抽样在$(-\infty,y]$中的概率和$(-\infty,x]$中的概率一致，就可以认为x的样本可以模拟y的样本。

### 例子

MATLAB自带的rand()函数可以生成从0到1之间的随机数。
$$
    X \sim U[0, 1]
$$

目标分布是：
$$
    Y \sim Exp(\lambda)
$$
$$
    f(y) = \lambda e^{-\lambda y} \quad y > 0
$$

根据
$$
    F(y) = \int_{-\infty}^{y} \lambda e^{-\lambda y} \mathrm{d}y
    = 1 - e^{-\lambda y}
    = \int_{0}^{x} \mathrm{d}x 
    = x
$$

得到随机变量$X$，转换到随机分布$Y$的关系式
$$
    y = -\frac{1}{\lambda} \ln(1-x)
$$

``` matlab
clear
%% 生成一组均匀分布的数组
X = rand(100000,1);

histogram(X,20,'Normalization','pdf'); 
grid on; grid minor;

t = title('产生的均匀分布数组的频率直方图');
t.FontSize = 13;
l = legend('频率直方图','理论概率密度曲线');
l.FontSize = 13;
hold off

%% 用均匀分布的数组生成指数分布的数组
lambda = 0.5;
Y = -1/lambda .* log(1 - X);

figure;
histogram(Y,40,'Normalization','pdf'); 
grid on; grid minor;

t = title('生成的指数分布数组的频率直方图');
t.FontSize = 13;
l = legend('频率直方图','理论概率密度曲线');
l.FontSize = 13;
hold off
```
