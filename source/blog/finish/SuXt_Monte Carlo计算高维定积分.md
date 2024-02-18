---
title: "Monte Carlo计算高维定积分"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: SuXt
tags:
  - 课程资料
  - 考试
  - 复习
summary: "Monte Carlo计算高维定积分"
author: "KhVeMx"
---

# Monte Carlo计算定积分

## 随机抽样数值计算定积分基本原理
$$
\int_a^b f(x) \mathrm{d}x \simeq \sum_i \xi_i f(x_i)
$$

数值定积分的计算方法是函数在区间内部采样的加权和。定积分的基本定义指出，对于一组任意分割的方法，只要权重和区间长度成正比，任意分割的最大区间的极限为0，那么得到的数值就是定积分的值。

为了计算方便，对于区间内部点的采样服从一定的概率分布$x_i \sim p(x)$，并且一般固定权重$\xi_i$。得到的关系为：
$$
\lim_{N\to\infty}\frac{b-a}{N}\sum_i f(x_i) \simeq \int_a^b f(x)p(x) \mathrm{d}x
$$
$$x_i \sim p(x)$$

## 随机抽样定积分误差分析

### 大数定理和中心极限定理
对于一个具有特定的平均值$\mu$和方差$\sigma^2$的概率模型。

大数定理：其**样本的平均值**随着样本数的增大依概率收敛到平均值上。

中心极限定理：其**样本的平均值**满足正态分布，平均值是$\mu$，方差是$\sigma^2/N$。
$$
\frac{1}{N} \sum_i f_i \sim N(\mu,\ \sigma^2/N)
$$

### 误差分析
$$\frac{1}{b-a}\int_a^b f(x) \mathrm{d}x \simeq \frac{1}{N}\sum_i f(x_i) \sim N(\mu,\ \sigma^2/N)$$
$$x_i \sim U(a,b)$$

求定积分的过程就其实就是在区间$(a,b)$内按照概率模型$\rho(x) = f(x)/(b-a)$采样得到一组样本$f(x_i)$。然后计算这组样本的平均值。

根据之前的分析，这样的操作符合大数定理和中心极限定理。所以得到的样本平均数就是概率模型$\rho(x)$的平均值。
$$\mu = E(\rho)=\int_a^b \rho(x) \mathrm{d}x = \frac{1}{b-a}\int_a^b f(x) \mathrm{d}x$$
$$\sigma^2 = D(\rho) = E(\rho^2) - E^2(\rho)$$

### 重要采样

当$x_i$依照概率分布$x_i \sim p(x)$
$$\frac{b-a}{N}\sum_i f(x_i) \simeq \int_a^b f(x)p(x) \mathrm{d}x$$
$$\frac{b-a}{N}\sum_i \frac{f(x_i)}{p(x_i)} \simeq \int_a^b f(x) \mathrm{d}x$$


## 例程

``` MATLAB
% 定义函数
f = @(x1, x2, x3, x4) sin(x1 + x2.^2 + 4.*x3 + x4.^2);

% 生成随机数
N = 100000; % 可以调整样本数以改变精度
samples = rand(N, 4); % 生成 N 个四维随机样本

% 采样
sample_values = arrayfun(@(i) f(samples(i, 1), samples(i, 2), samples(i, 3), samples(i, 4)), 1:N);

% 估计积分数值
integral_estimate = mean(sample_values);

```

### arrayfun()的使用
B = arrayfun(func,A1,...,An)
Apply function to each element of array

B = arrayfun(func,A1,...,An) applies func to the elements of the arrays A1,...,An, so that B(i) = func(A1(i),...,An(i)). The function func must take n input arguments and return a scalar. The arrays A1,...,An all must have the same size.


