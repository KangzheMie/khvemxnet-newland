---
title: "复化Simpson数值积分"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: WuLi
tags:
  - 课程资料
  - 考试
  - 复习
summary: "复化Simpson数值积分"
author: "KhVeMx"
---

# 复化Simpson数值积分

## Simpson数值积分
这是一种使用多项式插值的方法实现的积分。

在估计一个区间内的数值积分值的时候，有如下的一些情况

| 采样点数      | 多项式次数 | 形状|
| ----------- | :-----: | -----|
| 采样区间边值       | 0 | 矩形|
| 采样区间两边       | 1 | 梯形|
| 采样区间两边和中点 | 2  | 抛物线 |
|...|...|...|

然后估值可以通过对以上的几何图形的直接积分得到。并且由于多项式插值系数可以由采样值完全确定，所以积分的结果也由采样值完全确定。
$$\int_a^b f(x)\mathrm{d}x \simeq \frac{b-a}{6} \left[ f(a) + 4 f\left(\frac{a+b}{2}\right) + f(b) \right]$$


## 复化
复化是指，对于一个区间内部，将区间分成若干的等距的小区间，再在每个小区间使用多项式数值积分近似。


## 例程
``` c
#include <stdio.h>
#include <math.h>

double F(double x){return 1/sqrt(x);} // 被积函数

double Integral_Trapezoid(double (*f)(double x), double a, double b, int n){
    double h = (b - a) / (double)n;
    double sum = 0.0;

    for (int i = 1; i <= n-1; i++)  sum += (*f)(a + i*h);

    sum = h * (sum + 0.5*(*f)(a) + 0.5*(*f)(b));

    return sum;
}

double Integral_Simpson(double (*f)(double x), double a, double b, int m){
    int n = 2 * m;
    double h = (b - a) / (double) n;
    double sum = 0.0, sum_odd = 0.0, sum_even = 0.0;
    
    for(int i = 0; i <= m-1; i++)   sum_odd += (*f)(a + (2*i + 1)*h);
    for(int i = 1; i <= m-1; i++)   sum_even += (*f)(a + (2*i)*h);

    sum = h * ((*f)(a) + (*f)(b) + 4*sum_odd + 2 * sum_even) / 3;

    return sum;
}

int main(){
    printf("epsilon = 1e-6; m = 2147483647; I = %f\n",Integral_Simpson(F,1e-6,1,1e+4));
    return 0;
}
```