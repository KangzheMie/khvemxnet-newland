---
title: "常微分方程求解器"
date: "2024-02-16" # 格式为 YYYY-MM-DD
categories: SuXt
tags:
  - 课程资料
  - 考试
  - 复习
summary: "常微分方程求解器"
author: "ChatGPT"
---

# 常微分方程求解器

## 求解器目录

在 MATLAB 中，有多个用于解决常微分方程（ODEs）的函数，它们各自适用于不同类型的问题。以下是一些常用的 MATLAB ODE 解算器及其特点：

1. **ode45**：
   - 适用于大多数非刚性问题。
   - 基于显式 Runge-Kutta（4,5）公式。
   - 是初学者最常用的选择。

2. **ode23**：
   - 也适用于非刚性问题。
   - 基于显式 Runge-Kutta（2,3）配对公式。
   - 比 ode45 更快但可能不如其精确。

3. **ode113**：
   - 适用于非刚性问题。
   - 基于 Adams-Bashforth-Moulton 公式。
   - 适用于解平滑或者刚性较低的问题，对于高精度要求的长时间区间问题效果更好。

4. **ode15s**：
   - 适用于刚性问题和某些微分代数方程（DAEs）。
   - 基于数值微分公式（NDFs）。
   - 当问题存在快速变化的解时表现良好。

5. **ode23s**：
   - 适用于刚性问题。
   - 基于改进的 Rosenbrock 公式。
   - 对于中等精度要求的刚性问题是一个好的选择。

6. **ode23t**：
   - 适用于轻微刚性问题。
   - 基于梯形规则。
   - 当 ode45 遇到困难时是一个好的备选。

7. **ode23tb**：
   - 适用于刚性问题。
   - 基于梯形规则和后退差分公式。
   - 适用于较粗糙的刚性问题。

每种方法的选择依赖于问题的具体特性，例如问题的刚性、所需的精度、求解区间的长度等。通常，非刚性问题可以从使用 ode45 或 ode23 开始尝试，而刚性问题则可能需要使用 ode15s 或其他刚性求解器。在实践中，您可能需要尝试几种不同的方法来找到对您的特定问题最有效的求解器。


虽然 `ode15s` 可以处理 `ode45` 能处理的问题，包括非刚性和刚性问题，但这并不意味着 `ode15s` 总是 `ode45` 的最佳替代品。这两种方法各有优势和最适用的场景，选择哪一个取决于您正在解决的特定问题的性质。以下是两者的主要区别和优势：

### ode45
- **方法**：基于显式 Runge-Kutta (4,5) 方法。
- **适用情况**：主要用于求解非刚性问题。
- **优势**：
  - **速度**：对于非刚性问题，`ode45` 通常比 `ode15s` 更快，尤其是当问题可以通过较少的步骤解决时。
  - **简单性**：对于大多数常规的非刚性问题，`ode45` 是一个简单且高效的选择。

### ode15s
- **方法**：基于隐式数值微分方程（NDF）和后退微分方程（BDF）公式。
- **适用情况**：主要用于求解刚性问题和某些微分代数方程（DAE）。
- **优势**：
  - **适用范围**：能够有效处理刚性问题，这些问题在使用显式方法（如 `ode45`）时可能难以解决或需要非常小的时间步长。
  - **灵活性**：对于复杂的、具有挑战性的问题（如高度振荡的系统或含有刚性成分的系统），`ode15s` 提供了更好的稳定性和可靠性。

### 选择建议
- 对于大多数常规和非刚性的常微分方程问题，`ode45` 是一个很好的起点。它通常能够快速且有效地提供解决方案。
- 如果您发现使用 `ode45` 解决问题时需要非常小的步长，或者它无法有效地收敛到一个稳定的解，那么尝试 `ode15s` 是合理的，特别是当您怀疑问题可能具有刚性特性时。
- 对于刚性问题，`ode15s` 通常是更好的选择，因为它专门为处理这类问题而设计。

总结来说，虽然 `ode15s` 更加通用，但

在许多情况下，`ode45` 由于其对非刚性问题的高效性而成为首选。使用 `ode45` 和 `ode15s` 的关键是理解您的问题的性质以及选择最适合该问题的求解器。在实际应用中，您可能需要根据问题的特性和求解器的性能来做出选择。


## 求解器使用例程

很好，我可以为您提供四个 MATLAB 示例，分别展示如何使用 `ode45` 和 `ode15s` 来求解线性微分方程和方程组。每个示例都包含相应的微分方程（或方程组）定义，以及使用这些求解器的方法。

### 1. 使用 `ode45` 求解线性微分方程

#### 微分方程
考虑一个简单的一阶线性微分方程$\displaystyle \frac{dy}{dt} = -ay$，其中$\displaystyle a$ 是一个常数。

#### MATLAB 代码
```matlab
function dydt = odefun(t, y)
    a = 1;  % 定义常数 a
    dydt = -a * y;
end

[t, y] = ode45(@odefun, [0 5], 1); % 时间区间从 0 到 5，初始值为 1

plot(t, y);
xlabel('Time');
ylabel('Solution y');
title('Solution of linear ODE using ode45');
```

### 2. 使用 `ode15s` 求解线性微分方程

#### 微分方程
同样的方程$\displaystyle \frac{dy}{dt} = -ay$。

#### MATLAB 代码
```matlab
function dydt = odefun(t, y)
    a = 1;  % 定义常数 a
    dydt = -a * y;
end

[t, y] = ode15s(@odefun, [0 5], 1); % 时间区间从 0 到 5，初始值为 1

plot(t, y);
xlabel('Time');
ylabel('Solution y');
title('Solution of linear ODE using ode15s');
```

### 3. 使用 `ode45` 求解线性微分方程组

#### 微分方程组
考虑方程组$\displaystyle \frac{dy_1}{dt} = -3y_1 + 4y_2$，$\displaystyle \frac{dy_2}{dt} = -2y_1 + 3y_2$。

#### MATLAB 代码
```matlab
function dydt = odefun(t, y)
    dydt = zeros(2,1);    % 创建一个列向量
    dydt(1) = -3*y(1) + 4*y(2);
    dydt(2) = -2*y(1) + 3*y(2);
end

[t, y] = ode45(@odefun, [0 5], [1; 0]); % 时间区间从 0 到 5，初始值为 [1; 0]

plot(t, y);
xlabel('Time');
ylabel('Solutions y1 and y2');
title('Solution of linear ODE system using ode45');
```

### 4. 使用 `ode15s` 求解线性微分方程组

#### 微分方程组
同样的方程组$\displaystyle \frac{dy_1}{dt} = -3y_1 + 4y_2$，$\displaystyle\frac{dy_2}{dt} = -2y_1 + 3y_2$。

#### MATLAB 代码
```matlab
function dydt = odefun(t, y)
    dydt = zeros(2,1);    % 创建一个列向量
    dydt(1) = -3*y(1) + 4*y(2);
    dydt(2) = -2*y(1) + 3*y(2);
end

[t, y] = ode15s(@odefun, [0 5], [1; 0]); % 时间区间从 0 到 5，初始值为 [1; 0]

plot(t, y);
xlabel('Time');
ylabel('Solutions y1 and y2');
title('Solution of linear ODE system using ode15s');
```

在这些示例中，函数 `odefun` 定义了微分方程或方程组，`[t, y] = ode45(@odefun, [0 5], 1);` 和 `[t, y] = ode15s(@odefun, [0 5], 1);` 是调用求解器的代码行，其中 `ode45` 或 `ode15s` 是求解器的名称，`[0 5]` 是时间区间，`1` 是初始条件（对于方程组，是

一个初始条件向量）。最后，使用 `plot` 函数绘制了解的图形。


## 求解器解高次常系数线性方程


对于二阶或更高阶的微分方程，通常的做法是将其转换为一阶微分方程组。这是因为 MATLAB 的 ODE 求解器是设计来处理一阶微分方程组的。转换的基本思想是引入新变量来代表每个阶的导数。我将通过一个示例来展示如何进行这种转换和求解。

### 示例：将二阶微分方程转换为一阶方程组

假设我们有一个二阶微分方程，如下所示：

$$y''(t) + p y'(t) + q y(t) = g(t) $$

为了使用 MATLAB 的 ODE 求解器，我们可以将其转换为一阶微分方程组。我们引入 $\displaystyle u_1(t) = y(t)$ 和 $\displaystyle u_2(t) = y'(t)$，则原方程可转化为：

1. $\displaystyle u_1'(t) = y'(t) = u_2(t)$
2. $\displaystyle u_2'(t) = y''(t) = g(t) - p y'(t) - q y(t) = g(t) - p u_2(t) - q u_1(t)$

因此，原二阶方程等价于下面的一阶方程组：

$$
\begin{align}
u_1'(t) &= u_2(t) \\
u_2'(t) &= g(t) - p u_2(t) - q u_1(t) 
\end{align}
$$

#### MATLAB 代码示例
假设 $\displaystyle p = 1$，$\displaystyle q = 2$，并且 $\displaystyle g(t) = \sin(t)$，我们可以这样编写 MATLAB 代码：

```matlab
function dudt = odefun(t, u)
    p = 1;  % 定义 p
    q = 2;  % 定义 q
    g = sin(t); % 定义 g(t)
    dudt = [u(2); g - p*u(2) - q*u(1)];  % u(1) = y, u(2) = y'
end

[t, u] = ode45(@odefun, [0 10], [1; 0]); % 时间区间从 0 到 10，初始条件 y(0) = 1, y'(0) = 0

plot(t, u(:,1));
xlabel('Time');
ylabel('Solution y');
title('Solution of second order ODE using ode45');
```

在此代码中，`odefun` 定义了转换后的一阶方程组，`[t, u] = ode45(@odefun, [0 10], [1; 0]);` 调用 `ode45` 求解器来求解方程组，初始条件设置为 $\displaystyle y(0) = 1$ 和 $\displaystyle y'(0) = 0$。这个方法同样适用于更高阶的微分方程。


## 关于匿名函数

您提到的这种函数定义方式在 MATLAB 中被称为“匿名函数”（Anonymous Functions）。这是一种快捷而简洁的方法，用于创建小型的、无需额外文件的函数。匿名函数通常用于表示简单的数学表达式或执行小规模的操作。

### 匿名函数的基本结构
匿名函数的基本语法结构是：

```matlab
f = @(argument_list) expression;
```

其中 `f` 是函数句柄，`@(argument_list)` 定义了函数的输入参数（可以是多个参数），而 `expression` 是这些参数的函数体。例如：

```matlab
f = @(x) sin(x);
```

这行代码创建了一个函数 `f`，它接受一个参数 `x` 并返回 `sin(x)` 的值。

### 在 ODE 求解器中使用匿名函数
在使用如 `ode45` 这样的 ODE 求解器时，您可以通过匿名函数来定义微分方程。例如，考虑一阶微分方程 $\displaystyle y' = -2y$，您可以这样定义：

```matlab
dydt = @(t, y) -2 * y;
```

然后将这个函数句柄传递给 `ode45`：

```matlab
[t, y] = ode45(dydt, [0 5], 1);  % 时间区间从 0 到 5，初始值为 1
```

### 优点
- **简洁性**：匿名函数允许您在一行代码内定义函数，无需单独的函数文件。
- **便捷性**：适合定义简单的、一次性的函数，特别是在需要传递函数作为参数时（如传递给 ODE 求解器）。

### 限制
- **功能性**：由于它们的简洁性，匿名函数适用于简单的操作。对于更复杂的函数，创建标准的函数文件可能更合适。
- **局限性**：在匿名函数内部，您只能访问传入的参数和全局变量。匿名函数不能包含多行代码、循环或复杂的逻辑。

总结来说，匿名函数是 MATLAB 中一个非常方便的功能，特别适用于快速定义小型函数。在 ODE 求解器中使用匿名函数可以使代码更加简洁明了。