---
title: "求多项式方程的根以及误差的控制"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: SuXt
tags:
  - 课程资料
  - 考试
  - 复习
summary: "求多项式方程的根以及误差的控制"
author: "KhVeMx"
---

# 求多项式方程的根以及误差的控制
## 例子：求解五次勾股数

找出$x_1^5 + x_2^5 + x_3^5 + x_4^5 = x_5^5$整数解。其中
$$x_i\in \left \{ x \in \mathbb{Z} | 1 \le x \le 300  \right \},\space i = 1,2,3,4,5. $$

## 思路
设函数
$$
    F(x_1,x_2,x_3,x_4,x_5) = \sqrt[5]{x_1^5 + x_2^5 + x_3^5 + x_4^5} - x_5
$$

假设存在一组整数$[a,b,c,d,w]$，使得$F(a,b,c,d,w) = 0$则称这组整数是我们寻找的一组解。

考虑计算机产生的舍入误差，实际计算得到$F(a,b,c,d,w) = e$。设置误差限$\varepsilon$，当$|e|<\varepsilon$时则认为是一组有效解。

### 误差估计

分析误差限的大小：

计算机计算相近的整数组。
$$
    F(a,b,c,d,w) = e; \ F(a+1,b,c,d,w) = e'; \ F(a-1,b,c,d,w) = e''
$$

都可以得到接近0的数值，为了区分开来就需要合理设置误差限$\varepsilon$，使得
$$
    |e|<\varepsilon<\min\{e',e''\}
$$

因为变量$[x_1,x_2,x_3,x_4]$地位相同，所以只对$x_1$分析：
$$
    \frac{\partial F}{\partial x_1} = (x_1^5 + x_2^5 + x_3^5 + x_4^5)^{-\frac{4}{5}} x_1^4
$$
$$
    \Delta F \approx \frac{\partial F}{\partial x_1} \Delta x_1
    = (x_1^5 + x_2^5 + x_3^5 + x_4^5)^{-\frac{4}{5}} x_1^4 \Delta x_1
$$

由于${\partial F}/{\partial x_1}$关于变量$[x_2,x_3,x_4]$是减函数，关于变量$x_1$是增函数。考虑极端情况：
$$
    \frac{\partial F}{\partial x_1} 
    > \left . \frac{\partial F}{\partial x_1}\right |_{[x_1,x_2,x_3,x_4]=[1,300,300,300]}
    = (1 + 300^5 + 300^5 + 300^5)^{-\frac{4}{5}}
    \approx 5.126\times 10^{-11}
$$

计算机处理双精度的有效位数大概为15位，在处理百级的数值时，能保持的精度为$10^{-13}$。所以可以设置误差限$\varepsilon = 10^{-12}$。

### 程序展示

``` c
#include "stdio.h"
#include "math.h"

int judge(int *x5,int x1,int x2,int x3,int x4){
  double y,err;
  int a;
  //计算五次方和
  y = pow(x1,5)+pow(x2,5)+pow(x3,5)+pow(x4,5);
  //如果五次方和超过300^5 排除结果
  if(y > 2.43e12) return 0;
  else{
    y = pow(y,0.2);      //开5次方
    a = (int)(y + 0.5);  //四舍五入
    err = fabs(y - a);   //误差
    if(err < 1e-12 && a <= 300) //误差限1e-12
    {
      *x5 = a;
      return 1;
    } 
    else 
      return 0;
  }
}

int main(){
  int x1 = 1,x2 = 1,x3 = 1,x4 = 1,x5 = 1;

  for(x1 = 1; x1 <= 300; x1++)
    for(x2 = x1; x2 <= 300; x2++)
      for(x3 = x2; x3<= 300; x3++)
        for(x4 = x3; x4<= 300; x4++) 
          //生产一组不重复的整数[x1,x2,x3,x4]
          if(judge(&x5,x1,x2,x3,x4)) 
            printf("[%d,%d,%d,%d,%d]\n",x1,x2,x3,x4,x5);
  return 0;
}
```