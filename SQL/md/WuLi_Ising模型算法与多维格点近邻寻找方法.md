---
title: "Ising模型算法与多维格点近邻寻找方法"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: WuLi
tags:
  - 课程资料
  - 考试
  - 复习
summary: "Ising模型算法与多维格点近邻寻找方法"
author: "KhVeMx"
---

# Ising模型算法与多维格点近邻寻找方法

## Ising模型基本算法
计算的模型是一个格点长度$L$一定的一维二维三维正交晶格。

实际上每个格点的状态使用多维数组存储。最终计算的对象和输出的对象都是多维数组内部的值。

### Metropolis算法

- 定义格点长度$L$
- 根据模型的维度$d$生成格点的多维数组$L^d$，并约定在模型中使用周期边界条件。
- 初始化格点，让每一个格点拥有+1或者-1的随机初始值。
- 使用Metropolis算法
    - 首先随机选取一个格点
    - 计算这个格点变化自身自旋方向时的引起的能量变化
    - 如果能量变化为负数，说明这个变化使得系统向着更加稳定的方向演化，接收这个变化。
    - 如果能量变化为正数，那么将有一定的几率接收这样的变化，表示系统的热激发。
- 演化若干次后输出最终结果，认为此时已经达到了热平衡。
- 计算不同温度下的热平衡时的磁化率，并画出图像

### Metropolis算法说明

计算某个格点变化时，系统能量的变化，可以用下式
$$
\Delta E = 2J S_{i,j} \left( S_{i-1,j} + S_{i+1,j} + S_{i,j-1} + S_{i,j+1} \right)
$$

这个公式的含义是：如果 $S_{i,j}$ 与其最近邻的自旋方向相同，则翻转 $S_{i,j}$ 会增加系统能量；如果 $S_{i,j}$ 与其最近邻的自旋方向相反，则翻转 $S_{i,j}$ 会减少系统能量。

计算接收概率时，可以用下式
$$
    e^{-\Delta E / kT}
$$

对于每个自旋，计算翻转它所导致的能量变化$\Delta E$。
如果$\Delta E \leq 0$，则接受翻转（因为它降低了系统能量或保持不变）。
如果$\Delta E > 0$，则以概率$e^{-\Delta E / kT}$ 接受翻转，其中$k$是玻尔兹曼常数，$T$是温度。这允许系统以一定概率克服能量障碍，是热涨落的体现。

## 例程

``` matlab
% 参数设置
L = 20;                                         % 晶格尺寸
J1 = 1;                                         % 最近邻 相互作用常数
J2 = 1/sqrt(2);                                 % 次近邻 相互作用常数
nTimes = 10;                                    % 模拟次数
nSteps = 1e6;                                   % 热平衡迭代步数
T_min = 2;                                      % 最低温度
T_max = 7;                                      % 最高温度
T_size = 50;                                    % 温度数组的大小
Temperatures = linspace(T_min, T_max, T_size);  % 温度范围
Magnetizations = zeros(nTimes,T_size);          % 初始化磁化强度数组


for k = 1:nTimes
    % 重复若干次
    for i = 1:T_size
        % 求指定温度下的热稳态磁化强度
        Magnetizations(k,i) = Ising2D_2(Temperatures(i),L,J1,J2,nSteps);
    end
end

% 绘制磁化强度随温度的变化
plot(Temperatures, Magnetizations, 'o-');
xlabel('Temperature (T)');
ylabel('Magnetization (M)');
title('Magnetization vs. Temperature in 2D ising model');
grid on; grid minor;


% 只考虑最近邻影响的2维ising方程
function Magnetization = Ising2D(Temperature,L,J,nSteps)
    % 初始化晶格
    spinGrid = randi([0, 1], L, L) * 2 - 1; 
    % 仿真晶格的热平衡过程
    for step = 1:nSteps
        % 随机选择一个格点
        i = randi(L);
        j = randi(L);
        % 计算这个格点在翻转后的能量变化
        deltaE = 2 * J * spinGrid(i,j) * ...
            (spinGrid(i,mod(j-2,L)+1) + spinGrid(i,mod(j,L)+1) + ...
             spinGrid(mod(i-2,L)+1,j) + spinGrid(mod(i,L)+1,j));
        % 判定是否接收
        if deltaE <= 0 || rand() < exp(-deltaE / Temperature)
            spinGrid(i,j) = -spinGrid(i,j);
        end
    end
    % 计算磁化强度
    Magnetization = abs(mean(spinGrid, 'all'));
end

% 只考虑最近邻影响的3维ising方程
function Magnetization = Ising3D(Temperature,L,J,nSteps)
    % 初始化晶格
    spinGrid = randi([0, 1], L, L, L) * 2 - 1; 
    % 仿真晶格的热平衡过程
    for step = 1:nSteps
        % 随机选择一个格点
        i = randi(L);
        j = randi(L);
        k = randi(L);
        % 计算这个格点在翻转后的能量变化
        deltaE = 2 * J * spinGrid(i,j,k) * ...
        (spinGrid(mod(i-2,L)+1, j, k) + spinGrid(mod(i,L)+1, j, k) + ...
         spinGrid(i, mod(j-2,L)+1, k) + spinGrid(i, mod(j,L)+1, k) + ...
         spinGrid(i, j, mod(k-2,L)+1) + spinGrid(i, j, mod(k,L)+1));
        % 判定是否接收
        if deltaE <= 0 || rand() < exp(-deltaE / Temperature)
            spinGrid(i,j,k) = -spinGrid(i,j,k);
        end
    end
    % 计算磁化强度
    Magnetization = abs(mean(spinGrid, 'all'));
end

% 考虑次近邻影响情况下的2维ising模型
function Magnetization = Ising2D_2(Temperature,L,J1,J2,nSteps)
    spinGrid = randi([0, 1], L, L) * 2 - 1; % 初始化晶格

    % 达到热平衡
    for step = 1:nSteps
        i = randi(L);
        j = randi(L);
        deltaE = 2 * spinGrid(i,j) * ...
                (J1 * ( spinGrid(i,mod(j-2,L)+1) + ...
                        spinGrid(i,mod(j,L)+1)   + ...
                        spinGrid(mod(i-2,L)+1,j) + ...
                        spinGrid(mod(i,L)+1,j) ...
                    )  + ...
                J2 * ( spinGrid(mod(i-2,L)+1,mod(j-2,L)+1) + ...
                        spinGrid(mod(i-2,L)+1,mod(j,L)+1)   + ...
                        spinGrid(mod(i,L)+1,mod(j-2,L)+1)   + ...
                        spinGrid(mod(i,L)+1,mod(j,L)+1) ...
                    ) ...
                );
        if deltaE <= 0 || rand() < exp(-deltaE / Temperature)
            spinGrid(i,j) = -spinGrid(i,j);
        end
    end

    % 计算磁化强度
    Magnetization = abs(mean(spinGrid, 'all'));    
end
```


## 2D模型中的最近邻寻找方法

在 Ising 模型中，每个格点都有四个最近邻：上、下、左、右。为了处理位于边缘的格点，使用了模数运算（`mod`）来实现周期性边界条件。这意味着网格的一侧与另一侧相连。

考虑一个点 `(i, j)`，其最近邻为：
- 左邻点：`(i, mod(j-2, L) + 1)`
- 右邻点：`(i, mod(j, L) + 1)`
- 上邻点：`(mod(i-2, L) + 1, j)`
- 下邻点：`(mod(i, L) + 1, j)`

这里 `L` 是网格的大小，`mod` 操作确保索引值不会超出网格的边界。

```matlab
>> A

A =

     1     2     3     4     5

>> mod(A,5)

ans =

     1     2     3     4     0

>> mod(A-1,5)

ans =

     0     1     2     3     4

>> mod(A-2,5)

ans =

     4     0     1     2     3

>> mod(A-2,5) +1    % 求周期边界条件下的上一个点的姿势

ans =

     5     1     2     3     4

>> mod(A,5) + 1     % 求周期边界条件下的下一个点的姿势

ans =

     2     3     4     5     1
```

## 推广到一般的多维数组最近邻寻找方法

假设您有一个 n 维数组，每个维度的大小为 `sizeArray = [size1, size2, ..., sizeN]`，要找到点 `point = [p1, p2, ..., pN]` 的临近点，您可以对每个维度分别进行计算。

```matlab
    % 计算前后邻点
    prev_point(dim) = mod(point(dim) - 2, sizeArray(dim)) + 1;
    next_point(dim) = mod(point(dim), sizeArray(dim)) + 1;
```

### 直接使用例子
``` matlab
deltaE = 2 * spinGrid(i,j) * ...
        (J1 * ( spinGrid(i,mod(j-2,L)+1) + ...      % 左
                spinGrid(i,mod(j,L)+1)   + ...      % 右
                spinGrid(mod(i-2,L)+1,j) + ...      % 上
                spinGrid(mod(i,L)+1,j) ...          % 下
            )  + ...
        J2 * (  spinGrid(mod(i-2,L)+1,mod(j-2,L)+1) + ...   % 左上
                spinGrid(mod(i-2,L)+1,mod(j,L)+1)   + ...   % 右上
                spinGrid(mod(i,L)+1,mod(j-2,L)+1)   + ...   % 左下
                spinGrid(mod(i,L)+1,mod(j,L)+1) ...         % 右下
            ) ...
        );
```

``` matlab
% 随机选择一个格点
i = randi(L);       % 上下
j = randi(L);       % 左右
k = randi(L);       % 前后
% 计算这个格点在翻转后的能量变化
deltaE = 2 * J * spinGrid(i,j,k) * ...
    (   spinGrid(mod(i-2,L)+1,  j,              k) + ...            % 上
        spinGrid(mod(i,L)+1,    j,              k) + ...            % 下
        spinGrid(i,             mod(j-2,L)+1,   k) + ...            % 左
        spinGrid(i,             mod(j,L)+1,     k) + ...            % 右
        spinGrid(i,             j,              mod(k-2,L)+1) + ... % 后 纸面内
        spinGrid(i,             j,              mod(k,L)+1)         % 前 纸面外
    );
```