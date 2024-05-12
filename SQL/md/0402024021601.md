---
title: "精确对角化"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: WuLi
tags:
  - 课程资料
  - 考试
  - 复习
summary: "精确对角化"
author: "KhVeMx"
---

# 精确对角化

精确对角化实际上`就是把哈密顿量写成矩阵`表示，然后再求这个矩阵的最小本征值和本征矢，也就是基态和基态能量。

说人话就是每一个工科生都会的矩阵力学求解本征值和本征向量的过程。

而本文的所有内容都在探究，如何构造矩阵。

构造矩阵无非两种方法
1. 通过算符在某表象下的矩阵形式和直积直接构造矩阵
2. 通过在某表象下的波矢于算符的定义计算$\langle m|H|n \rangle$

## 自旋模型的哈密顿算符精确对角化

### 自旋算符简介

在量子力学中，自旋算符 $S^x$, $S^y$, 和 $S^z$ 分别对应自旋沿x, y, z轴的分量。对于一个自旋1/2粒子，自旋升降算符 $S^+$ 和 $S^-$ 可以用来提升或降低自旋的z分量。这些算符之间的关系如下：

- $S^+ = S^x + iS^y$
- $S^- = S^x - iS^y$

这里的 $S^+$ 和 $S^-$ 是升降算符，它们可以将自旋态 $\lvert \downarrow \rangle$ 和 $\lvert \uparrow \rangle$ 转换为：

- $S^+ \lvert \downarrow \rangle = \hbar \lvert \uparrow \rangle$
- $S^- \lvert \uparrow \rangle = \hbar \lvert \downarrow \rangle$

而 $S^x$, $S^y$, $S^z$ 与基态 $\lvert \uparrow \rangle$ 和 $\lvert \downarrow \rangle$ 的作用如下：

- $S^z \lvert \uparrow \rangle = \hbar/2 \lvert \uparrow \rangle$
- $S^z \lvert \downarrow \rangle = -\hbar/2 \lvert \downarrow \rangle$
- $S^x$ 和 $S^y$ 将会在基态之间产生叠加。

在自旋表象下，算符的矩阵形式如下：

- $S^z$ 算符的矩阵表示为：
  $$
  S^z = \frac{\hbar}{2} \begin{pmatrix}
  1 & 0 \\
  0 & -1
  \end{pmatrix}
  $$
- $S^+$ 算符的矩阵表示为：
  $$
  S^+ = \hbar \begin{pmatrix}
  0 & 1 \\
  0 & 0
  \end{pmatrix}
  $$
- $S^-$ 算符的矩阵表示为：
  $$
  S^- = \hbar \begin{pmatrix}
  0 & 0 \\
  1 & 0
  \end{pmatrix}
  $$

对于 $S^x$ 和 $S^y$ 算符，可以通过 $S^+$ 和 $S^-$ 表达为：

- $S^x = \frac{1}{2}(S^+ + S^-)$ 算符的矩阵表示为：
  $$
  S^x = \frac{\hbar}{2} \begin{pmatrix}
  0 & 1 \\
  1 & 0
  \end{pmatrix}
  $$
- $S^y = \frac{1}{2i}(S^+ - S^-)$ 算符的矩阵表示为：
  $$
  S^y = \frac{\hbar}{2i} \begin{pmatrix}
  0 & -i \\
  i & 0
  \end{pmatrix}
  $$


### 需要对角化的费米子哈密顿算符

$$ H = -J \sum_{i=1}^{N} \vec{S}_i \cdot \vec{S}_{i+1} = -J \sum_{i=1}^{N} \left( S_i^x S_{i+1}^x + S_i^y S_{i+1}^y + S_i^z S_{i+1}^z \right) $$

可以重新表达为：

$$ H = -J \sum_i \left[ \frac{1}{2}(S^+_i S^-_{i+1} + S^-_i S^+_{i+1}) + \frac{1}{2i}(S^+_i S^-_{i+1} - S^-_i S^+_{i+1}) + \Delta S_{zi} S_{z(i+1)} \right] $$

$$ H = -J \sum_{i=1}^{N} \left[ \frac{1}{2} \left( S_i^+ S_{i+1}^- + S_i^- S_{i+1}^+ \right) + S_i^z S_{i+1}^z \right] $$

### 通过张量积构造矩阵

例程

``` matlab
function H = tensor_product(varargin)   % varargin 接收变长参数
    if length(varargin) < 2
        H = varargin{1};
        return
    end

    H = varargin{1};
    for i = 2:length(varargin)
        H = kron(H, varargin{i});
    end
end

Sz = [1, 0; 0, -1] ./ 2;
Sp = [0, 1; 0,  0];
Sm = [0, 0; 1,  0];
II = eye(2);
``` 

有了上边的直积工具以及矩阵，就可以构造哈密顿矩阵了

$$ \frac{1}{2} \sum_{i} \left( S_i^+ S_{i+1}^- + S_i^- S_{i+1}^+ \right) 
+ \sum_{i} S_i^z S_{i+1}^z
$$

``` matlab
H = 1/2 * ( ...
      tensor_product(Sp, Sm, II, II) ...
    + tensor_product(II, Sp, Sm, II) ...
    + tensor_product(II, II, Sp, Sm) ...
    + tensor_product(Sm, II, II, Sp) ...    % 这里是周期，边界开放将这个删除
                                     ...
    + tensor_product(Sm, Sp, II, II) ...
    + tensor_product(II, Sm, Sp, II) ...
    + tensor_product(II, II, Sm, Sp) ...
    + tensor_product(Sp, II, II, Sm) ...    % 这里是周期，边界开放将这个删除
    ) + (                            ...
      tensor_product(Sz, Sz, II, II) ...
    + tensor_product(II, Sz, Sz, II) ...
    + tensor_product(II, II, Sz, Sz) ...
    + tensor_product(Sz, II, II, Sz) ...    % 这里是周期，边界开放将这个删除
    );
```

**注意！！！！**

本处将所有的$\hbar = 1$，忽略所有的$\Delta$和$J$。


### 通过基矢和算符计算构造矩阵

比如考虑有4个自旋的系统，他的所有基矢表示为：
$$ \lvert 0 \rangle = \lvert \uparrow \uparrow \uparrow \uparrow \rangle = (0000) $$
$$ \lvert 1 \rangle = \lvert \uparrow \uparrow \uparrow \downarrow \rangle = (0001) $$
$$ \lvert 2 \rangle = \lvert \uparrow \uparrow \downarrow \uparrow \rangle = (0010) $$
$$ \lvert 3 \rangle = \lvert \uparrow \uparrow \downarrow \downarrow \rangle = (0011) $$
$$ \cdots $$

然后根据哈密顿算符的定义计算哈密顿量的矩阵元
$$ H_{mn} = \langle m \lvert H \lvert n \rangle $$

计算例子：
$$
\begin{aligned}
H \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle 
&= -J \sum_i \left[ \frac{1}{2} \left( S_i^+ S_{i+1}^- + S_i^- S_{i+1}^+ \right) + \Delta S_i^z S_{i+1}^z \right] \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle \\
&= -\frac{J}{2} \left( S_1^+ S_2^- + S_2^+ S_3^- + S_3^+ S_4^- + S_4^+ S_5^-\right) \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle \\
&\ \ \ \  -\frac{J}{2} \left( S_1^- S_2^+ + S_2^- S_3^+ + S_3^- S_4^+ + S_4^- S_5^+\right) \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle \\
&\ \ \ \  -J \Delta \left( S_1^z S_2^z + S_2^z S_3^z + S_3^z S_4^z + S_4^z S_5^z \right) \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle \\
&= -\frac{J}{2} \lvert \uparrow \downarrow \uparrow \downarrow \downarrow \rangle 
- J \Delta \left( \frac{1}{4} - \frac{1}{4} - \frac{1}{4} + \frac{1}{4} \right) \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle \\
&= -\frac{J}{2} \lvert \uparrow \downarrow \uparrow \downarrow \downarrow \rangle  - \frac{J \Delta}{2} \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle
\end{aligned}
$$

**注意！！！！** 本处将所有的$\hbar = 1$

从上边的例子可以看出，H的求和符号代表的是哈密顿算符本身的构造。所以基矢需要和所有构造的内容都进行一遍相互作用。最明显的就是

$$
-J \sum_i \Delta S_i^z S_{i+1}^z \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle
= - J \Delta \left( \frac{1}{4} - \frac{1}{4} - \frac{1}{4} + \frac{1}{4} \right) \lvert \uparrow \uparrow \downarrow \downarrow \downarrow \rangle
$$

### 例程：

``` matlab
N = 4;
% 初始化哈密顿矩阵
H = zeros(2^N, 2^N);

% 遍历所有基矢
%{
    对于这个系统来说，所有的状态都可以用二进制完全表示
    如从0000 ~ 1111表示N = 4时的所有基矢的状态
    生成哈密顿量矩阵的步骤就是根据这些基矢和哈密顿算符的定义
    写出所有矩阵元上的元素

    遍历基矢|a>
    例如从|0000> ~ |1111>
%}
for a = 0:(2^N - 1)
    % 对每个基矢 |a> 根据上边的计算例子，计算他对于哈密顿矩阵的贡献
    %{
        基矢本身由N个元素组成
        |XOXX> |XXOX>
          ^       ^
          i       j

        然后再检查基矢的组成是否可以满足算符的条件
        根据基矢的组成可以求得对于各个矩阵元的贡献
    %}
    for i = 0:(N - 1)
        % 只考虑i的下一个邻位
        j = mod(i+1, N);

        % 获取|a>态的第i位的值
        ai = get_state_index(a, i);
        % 获取|a>态的第j位的值
        aj = get_state_index(a, j);

        % Sz项
        %{
            S^z_i S^z_i+1 算符不改变状态，但是会产生系数1/2
            S^z |1> =  1/2 |1>
            S^z |0> = -1/2 |1>

            由于算符不改变状态，所以在计算<m|H|n>时只有对角元<n|n>有效
        %}
        if ai == aj                             
            % 当ij同向，±1/2 * ±1/2 = 1/4
            % 注意！！！！ 这里具体+什么，需要根据H的具体构造
            H(a+1, a+1) = H(a+1, a+1) + 0.25;
        else
            % 否则当ij反向时，-1/4
            % 注意！！！！ 这里具体+什么，需要根据H的具体构造
            H(a+1, a+1) = H(a+1, a+1) - 0.25;
        end

        % SxSx + SySy项
        %{
            S^p_i S^n_i+1 算符会改变状态|a>到|b>
            S^p_i S^n_i+1 |01> = 1/2 |10>
            <b|S^p_i S^n_i+1|a> = 1/2 <b|a>

            当a = |10> S^p_i S^n_i+1无效 S^n_i S^p_i+1有效
            当a = |01> S^p_i S^n_i+1有效 S^n_i S^p_i+1无效
        %}
        if ai ~= aj
            % a = |10> -> b = |01>
            % a = |01> -> b = |10>
            b = flip_state(a, i);
            b = flip_state(b, j);
            %{ 
                最终无论是S^p_i S^n_i+1有效还是S^n_i S^p_i+1有效
                最终<b|H|a>的矩阵元还是1/2
            %}

            % 注意！！！！ 这里具体+什么，需要根据H的具体构造
            H(a+1, b+1) = H(a+1, b+1) + 0.5; 
        end
    end
end

function index = get_state_index(state, position)
    % 获取state在指定position的二进制值
    mask = bitshift(1, position);
    index = bitand(state, mask);
    index = bitshift(index, -position);
end

function new_state = flip_state(state, position)
    % 翻转state在指定position的二进制值
    mask = bitshift(1, position);
    new_state = bitxor(state, mask);
end
```

如果不考虑周期边界，那么在邻位j处增加一个判断。
``` MATLAB
for i = 0:(N - 1)
    % 只考虑i的下一个邻位
    j = i+1;
    
    if j == N
        break;
    else
        % 宇宙星光灿烂
    end
end
```

## 截断法

粒子的希尔伯特空间是$2^N$，精确对角化在多个粒子的时候有巨大的限制。

考虑限制粒子数量为少量的几个，这样可以得到靠近基态的一些能量分布。这是因为认为多数的粒子占据态对于基态能量的贡献不大。

因为是认为截断精度，所以称之为截断法，产生的误差是截断误差。

### 例程：
``` matlab
% 参数设置
L = 5;  % 链的长度
N = 2;  % 处于激发态的粒子数
J = 1;  % 相互作用强度
Delta = 1;  % 自旋相互作用参数

% 生成所有可能的状态
% 这里有从1:L中选N的所有组合，作为激发粒子的坐标
states = nchoosek(1:L, N);

% 初始化哈密顿矩阵
num_states = size(states, 1);
H = zeros(num_states, num_states);

% 填充哈密顿矩阵
for i = 1:num_states
    % 根据激发粒子的坐标，生成类似[0 1 1 0 0]的态 计为|i>
    current_state = zeros(1, L);
    current_state(states(i, :)) = 1;
    
    % 根据激发粒子的坐标，生成类似[0 1 0 1 0]的态 计为|j>
    for j = 1:num_states
        next_state = zeros(1, L);
        next_state(states(j, :)) = 1;

        % 根据之前的|i>!=|j> 以及要求的H，写出矩阵元<i|H|j>
        % 检查 S+ S- 和 S- S+ 项

        % 根据|i>|j>态中的每一项进行判断
        for k = 1:(L-1)
            % 如果发现两个态之间满足跃迁关系 |01> or |10>
            if current_state(k) ~= current_state(k+1)
                % 那么将current_state跃迁到态temp_state
                temp_state = current_state;
                temp_state([k, k+1]) = temp_state([k+1, k]); % 交换相邻自旋

                %如果跃迁后的temp_state与|j>相同
                if all(next_state == temp_state)
                    H(i, j) = H(i, j) - 0.5 * J;
                end
            end
        end
    end

    % 根据之前的|i> 以及要求的H，写出矩阵元<i|H|i>
    % 计算对角线上的 S_z S_z 项
    for k = 1:(L-1)
        H(i, i) = H(i, i) - Delta * (2*current_state(k)-1) * (2*current_state(k+1)-1) / 4;
    end
    
end

% 显示哈密顿矩阵
heatmap(H);
```

### 截断法求解费米子体系
$$
H = -J\sum_i (c_i^\dagger c_{i+1} + h.c.) + Un_in_{i+1} - \mu n_i
$$

``` matlab
% 参数设置
L = 5;  % 链的长度
N = 2;  % 处于激发态的粒子数

J = 0;  % 相互作用强度
U = 1;
mu = 0;  % 自旋相互作用参数

% 生成所有可能的状态
% 这里有从1:L中选N的所有组合，作为激发粒子的坐标
states = nchoosek(1:L, N);

% 初始化哈密顿矩阵
num_states = size(states, 1);
H = zeros(num_states, num_states);

% 填充哈密顿矩阵
for i = 1:num_states
    % 根据激发粒子的坐标，生成类似[0 1 1 0 0]的态 计为|i>
    current_state = zeros(1, L);
    current_state(states(i, :)) = 1;
    
    % 根据激发粒子的坐标，生成类似[0 1 0 1 0]的态 计为|j>
    for j = 1:num_states
        next_state = zeros(1, L);
        next_state(states(j, :)) = 1;

        % 根据之前的|i>!=|j> 以及要求的H，写出矩阵元<i|H|j>

        % 根据|i>|j>态中的每一项进行判断
        for k = 1:(L-1)  % 这个k的遍历范围非常重要！！！
            % 如果发现两个谐振子之间满足可跃迁关系 |01> or |10>
            if current_state(k) ~= current_state(k+1)
                % 那么将current_state跃迁到态temp_state
                temp_state = current_state;
                temp_state([k, k+1]) = temp_state([k+1, k]); % 交换相邻自旋

                %如果跃迁后的temp_state与|j>相同
                if all(next_state == temp_state)
                    H(i, j) = H(i, j) - J;
                end
            end
        end
    end

    for k = 1:(L-1)     % 这个k的遍历范围非常重要！！！
        % 如果发现两个谐振子满足相邻关系
        if current_state(k) == 1 && current_state(k+1) == 1
            H(i,i) = H(i,i) + U;
        end
    end

    for k = 1:L         % 这个k的遍历范围非常重要！！！
        % 如果发现有谐振子的存在
        if current_state(k) == 1
            H(i,i) = H(i,i) - mu;
        end
    end
    
end

% 显示哈密顿矩阵
heatmap(H);
```

当考虑周期边界条件时：
```matlab
% 根据|i>|j>态中的每一项进行判断
for k = 1:L     % 这个k的遍历范围非常重要！！！
    % 如果发现两个谐振子之间满足可跃迁关系 |01> or |10>
    if current_state(k) ~= current_state(mod(k-2,L)+1)
        % 那么将current_state跃迁到态temp_state
        temp_state = current_state;
        temp_state([k, mod(k-2,L)+1]) = temp_state([mod(k-2,L)+1, k]); % 交换相邻自旋

        %如果跃迁后的temp_state与|j>相同
        if all(next_state == temp_state)
            H(i, j) = H(i, j) - J;
        end
    end
end
```