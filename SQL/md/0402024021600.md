---
title: "有限差分法解波函数"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: WuLi
tags:
  - 课程资料
  - 考试
  - 复习
summary: "有限差分法解波函数"
author: "KhVeMx"
---

# 有限差分法解波函数

## 一维方程

一维薛定谔波动方程为： 
$$\hat{H}\psi(x) = \left[ 
        -\frac{\hbar^2}{2m}\frac{\mathrm{d}^2}{\mathrm{d}x^2}
        + V(x) \right] \psi(x)
    = E \psi(x)$$

这里举例用最简单的无限深势阱模型来做数值计算的验证。此时量子的势函数为：
$$
V(x) = 
    \begin{cases} 
        \displaystyle 0\ \qquad |x|<\frac{a}{2} \\
        \displaystyle \infty \qquad |x| \geq \frac{a}{2}
\end{cases}
$$

所以有: 
$$\psi(\pm \frac{a}{2}) = 0$$

有解析解： 
$$
\psi_n(x) = \begin{cases}
    \displaystyle \sqrt{\frac{2}{a}}\cos\frac{n\pi x}{a}, \quad n\ in\ odd\\
    \displaystyle \sqrt{\frac{2}{a}}\sin\frac{n\pi x}{a}, \quad n\ in\ even
\end{cases}
$$

波函数$\psi_n(x)$对应的能级为：
$$E_n = \frac{n^2 \pi^2 \hbar^2}{2 m a^2}$$

用有限差分法，将上述的微分方程模型离散化。求本征函数和本征值的问题，转化为了矩阵的本征值和本征向量的问题。

此时哈密顿算符可以表示为以下的形式： 
$$
\mathbf{\hat{H} \psi } 
=
\left(
-\frac{\hbar^2}{2m(\delta x)^2} 
\begin{bmatrix}  
  -2 & 1 & \cdots & 0 \\  
  1 & -2 & \cdots & 0 \\  
  \vdots & \vdots & \ddots & \vdots \\  
  0 & 0 & \cdots & -2  
\end{bmatrix}
+ \begin{bmatrix}  
  V_1 & 0 & \cdots & 0 \\  
  0 & V_2 & \cdots & 0 \\  
  \vdots & \vdots & \ddots & \vdots \\  
  0 & 0 & \cdots & V_n  
\end{bmatrix} 
\right)
\begin{bmatrix}
 \psi_1\\
 \psi_2\\
 \vdots\\
 \psi_n
\end{bmatrix}
=
E \psi
$$

设置一个参数$\displaystyle E_R = \frac{\hbar^2}{2m(\delta x)^2}$具有能量的量纲。

``` matlab
% 本函数用于仿真指定势能函数的一维量子点波函数
hbar = 1.05457168e-34; % J s
m = 0.1 * 9.1093826e-31; % kg
dx = 0.1 * 1e-9; % m
eV = 1.60217653e-19; % J
E_R = (hbar^2/(2*m*dx^2))/eV; % eV
N = int32(100 * 1e-9 / dx);
x = linspace(-50,50,N); % nm
V = zeros(N, 1); 

% 势能 eV
V(1:400) = 1;
V(400:500) = linspace(1,0,101);
V(500:600) = linspace(0,1,101);
V(600:1000) = 1;

% 哈密顿算子
H = E_R * (2 * eye(N) - diag(ones(N-1,1), 1) - diag(ones(N-1,1), -1)) +
diag(V);

% 本征值和本征波函数
[psi, E] = eig(H);
E = diag(E);
E(1:10)
subplot(211);plot(x,psi(:,4));
title('一维量子点波函数（未归一化） ');
xlabel('长度/nm');
grid on; grid minor;
legend('\psi_4(x)');
subplot(212);plot(x,V);
title('势函数');
xlabel('长度/nm'); ylabel('能量/eV');
grid on; grid minor;
```

## 二维方程

二维的定态薛定谔方程是：
$$
    \hat{H}\psi(x,y) = \left[ 
        -\frac{\hbar^2}{2m}\left(
        \frac{\partial^2}{\partial x^2}
        + \frac{\partial ^2}{\partial y^2}\right)
        + V(x,y) \right] \psi(x,y)
    = E \psi(x,y)
$$

因为是二维的波函数，本来波函数是二维矩阵，这样不利于我们求本征值和本征向量。所以将正方形中的波函数逐行放入到一个向量之中。如果正方形被分割成了$N\times N$个点，那么这个向量就有$N\times N$行$1$列。

此时二阶求导算符以及哈密顿算符的规模就是$N\times N$行$N\times N$列。
根据点是在边界还是在内部可以构造出二阶求导算符，配合势能函数最终组成哈密顿算符。

参考一维的波函数解法：
$$
    \mathbf{\hat{H} \psi} = (E_R \mathbf{\hat{D}}
    + \mathbf{\hat{V}}) \psi
    = E \psi
$$

其中:
$$
    E_R = \frac{\hbar^2}{2m\delta^2}
$$

``` matlab
% 本函数用于仿真指定二维势函数下的二维量子波函数和对应的能量本征值
clc
clear
close all

% 参数
hbar = 1.05457168e-34; % J s
m = 9.1093826e-31; % kg
L = 10 * 1e-9; % nm
N = 50; % 二维网络各维度栅格点数
d = L / N; % nm
eV = 1.60217653e-19; % J
E_R = hbar^2/(2*m*d^2)/eV; % eV

% 将二维的波函数视作为(N*N,1)的向量，此时需要构造该向量的微分算符 D
D = zeros(N * N, N * N);
for i = 1:N
  for j = 1:N
      idx = (i - 1) * N + j; %(N*N,1)向量中第 idx 个点（i 行 j 列）
      D(idx, idx) = 4; %本身
    if i > 1 %如果不在上边界，有向上的差分
      D(idx, idx - N) = -1;
    end
    if i < N %如果不在下边界，有向下的差分
      D(idx, idx + N) = -1;
    end
    if j > 1 %如果不在左边界，有向左的差分
      D(idx, idx - 1) = -1;
    end
    if j < N %如果不在右边界，有向右的差分
      D(idx, idx + 1) = -1;
    end
  end
end

% 势函数
V = zeros(N*N,N*N);
for i = 1:N
  for j = 1:N
      idx = (i - 1) * N + j;
    if sqrt((i-N/2)^2+(j-N/2)^2) < 20
      V(idx,idx) = 0;
    else
      V(idx,idx) = 1e+10;
    end
  end
end

% 哈密顿算符
H = E_R * D + V;

% 求解薛定谔方程的本征值和本征矢
[psi, E] = eig(H);
E = diag(E);


%% 绘制
% 势函数
V = reshape(diag(V),N,N);
surf(V);title('势函数/eV');

% 绘制波函数
figure;
x = linspace(0, L, N);
y = linspace(0, L, N);
[X, Y] = meshgrid(x, y);

psi2D_1 = reshape((-psi(:, 1)), N, N);
psi2D_3 = reshape((psi(:, 3)), N, N);
psi2D_6 = reshape((-psi(:, 6)), N, N);
psi2D_7 = reshape((psi(:, 7)), N, N);

subplot(221);surf(psi2D_1);
title(['基态波函数', 'E_1 = ',num2str(E(1)),'eV']);
subplot(222);surf(psi2D_3);
title(['E_3 波函数' , 'E_3 = ',num2str(E(3)),'eV']);
subplot(223);surf(psi2D_6);
title(['E_6 波函数' , 'E_6 = ',num2str(E(6)),'eV']);
subplot(224);surf(psi2D_7);
title(['E_7 波函数' , 'E_7 = ',num2str(E(7)),'eV']);
```


