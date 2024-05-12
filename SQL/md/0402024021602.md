---
title: "统计系综的本征值间距分布"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: WuLi
tags:
  - 课程资料
  - 考试
  - 复习
summary: "统计系综的本征值间距分布"
author: "KhVeMx"
---

# 统计系综的本征值间距分布

## 基础知识

### 系综

研究多粒子的宏观系统，实际上只能测量到的物理量是一些宏观量，比如说粒子总数、压强、温度。而实际上有大量的微观状态可以对应这些宏观量。

系综是「具有相同宏观性质但处于不同微观状态的**系统的集合**」。

### 高斯系综

高斯统计系综可以用实对称的随机矩阵表示，是因为这种表示法能够捕捉到物理系统在统计平均意义上的性质，尤其是当系统的微观状态遵循高斯分布时。实对称随机矩阵在理论上是方便的，因为它们的数学性质使得能够较容易地分析系统的统计行为。

## 统计系综的本征值间距分布

以下讨论的所有分布，其间距实际上做了归一化处理
$$
    \frac{s}{\left\langle s \right\rangle} \to s
$$

泊松系综的热力学极限
$$
    P(\tilde{s} ) = e^{-\tilde{s}}
$$

---

高斯正交系综的随机矩阵可以通过如下的公式生成：
$$
    H = \frac{A+A^T}{2}
$$

其中$A$矩阵中的元素都满足标准正态分布$N(0,1)$

$$
    P_{\text{GOE}}(s) = \frac{\pi s}{2} e^{-\frac{\pi s^2}{4}}
$$

---

高斯酉系综（GUE）可以通过如下的公式生成：
$$
    H = \frac{A+A^\dagger}{2}
$$

其中$A$根据以下方法生成
$$
    A = \mathrm{randn()} + i * \mathrm{randn()}
$$

$$
    P_{\text{GUE}}(s) = \frac{32 s^2}{\pi^2} e^{-\frac{4 s^2}{\pi}}
$$

---

``` matlab
for i = 1:num_matrices
    % 假设这是泊松系综得到的特征值分布
    E = rand(N,1);
    % 排序求差
    s(:,i) = diff(sort(E));
end
```

``` matlab
% GOE GUE
N = 2;                              % 设置矩阵大小
num_matrices = 100000;              % 生成的矩阵数量8
eig_GOE = zeros(N,num_matrices);
eig_GUE = zeros(N,num_matrices);
s_GOE = zeros(N-1,num_matrices);
s_GUE = zeros(N-1,num_matrices);

% 生成高斯系综的随机矩阵
for k = 1:num_matrices
    A = randn(N);
    H = (A+A')/2;
    % 将H矩阵的所有特征值排序后取临近差分
    E = eig(H);
    eig_GOE(:,k) = E;  
    s_GOE(:,k) = diff(sort(E));
end

% 生成高斯酉系综的随机矩阵
for k = 1:num_matrices
    A = randn(N) + 1i*randn(N);
    H = (A+A')/2;
    % 将H矩阵的所有特征值排序后取临近差分
    E = eig(H);
    eig_GUE(:,k) = E;  
    s_GUE(:,k) = diff(sort(E));
end

% 取s_GUE的实部，舍去虚部的计算噪声
s_GUE = real(s_GUE);

% 对s数据整形并求出均值和平方均值
s_GOE = s_GOE(1:end);
s_GUE = s_GUE(1:end);
s_GOE_mean = mean(s_GOE);
s_GUE_mean = mean(s_GUE);
s2_GOE_mean = var(s_GOE) + s_GOE_mean^2;
s2_GUE_mean = var(s_GUE) + s_GUE_mean^2;

% 计算s数据的均值并做均值归一化处理
s_GUE = s_GUE ./ s_GUE_mean;
s_GOE = s_GOE ./ s_GOE_mean;

% 两种系综的特征值间隔分布的解析结果
x = linspace(0,3.5,200);
p_GOE = @(x) pi .* x ./2 .* exp(- pi .* x .^2 ./ 4);
p_GUE = @(x) 32 .* x.^2 ./pi^2 .* exp(- 4 .* x .^2 ./ pi);


% 统计并画出s的直方图
histogram(s_GUE, 100,'Normalization','pdf'); hold on
histogram(s_GOE, 100,'Normalization','pdf');
title('特征值间距分布');
xlabel('s');
ylabel('P(s)');
grid on; grid minor;

plot(x,p_GOE(x),'LineWidth',3);
plot(x,p_GUE(x),'LineWidth',3);

legend("GUE \beta = 2","GOE \beta = 1","GOE \beta = 1","GUE \beta = 2");

hold off
```

