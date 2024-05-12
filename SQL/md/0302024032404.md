---
title: "MATLAB绘图专栏"
date: "2024-03-24" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - MATLAB
  - plot
summary: "MATLAB绘图"
author: "ChatGPT"
---

# MATLAB绘图

关于绘图函数、句柄参数的信息请参考如下的matlab文档：

「Axes Properties」：坐标轴

「Line Properties」：plot函数

「ErrorBar Properties」：ErrorBar函数

....

## 优化坐标轴可视参数

```matlab
function customizeAxes(ax)
    % 检查输入是否为轴对象
    if ~isa(ax, 'matlab.graphics.axis.Axes')
        error('Input must be an axes object');
    end
    
    % 设置轴的属性
    ax.XLim = [150 550]; % X轴范围
    ax.FontSize = 16; % 字体大小
    ax.XGrid = 'on'; % 开启X轴网格
    ax.YGrid = 'on'; % 开启Y轴网格
    ax.XMinorGrid = 'on'; % 开启X轴次级网格
    ax.YMinorGrid = 'on'; % 开启Y轴次级网格
    ax.GridColor = [0 0 0]; % 网格颜色
    ax.GridAlpha = 0.2; % 网格透明度
    ax.MinorGridColor = [0 0 0]; % 次级网格颜色
    ax.MinorGridAlpha = 0.2; % 次级网格透明度
    ax.LineWidth = 1.0; % 线宽
end
```

## 绘制平均值-标准差-最值图像

``` matlab
function mean_std_plot(X,Y_mean,Y_std,Y_max,Y_min)

    % 确定生成出来的图像框的位置和大小
    figure('Position', [100, 100, 1200, 850]);
    
    hold on;

    % 插值并绘制曲线
    xInterp = linspace(min(X), max(X), 100);
    yInterp = interp1(X, Y_mean, xInterp, 'spline');
    plot(xInterp, yInterp, '--k');

    % 绘制最大值到最小值的线段
    for i = 1:length(X)
        plot([X(i), X(i)], [Y_min(i), Y_max(i)], '-r','LineWidth',1.1); % 使用黑色线段表示最值范围
    end

    % 绘制散点图和误差条
    errorbar(X, Y_mean, Y_std,'xb','LineWidth',1.1,'MarkerSize',5,'CapSize',10);
       
    grid on;
    grid minor;
    hold off;
end
```

## 绘制热力图
``` matlab
figure('Position', [100, 100, 500, 500]);
h = heatmap(Amean);
h.XData = {'CH1','CH2','CH3'};
h.YData = {'#1','#3','#4','#5'};
h.Title = "数据平均值";
h.XLabel = "通道";
h.YLabel = "编号";
h.FontSize = 16;
```

## 绘制bar图
``` matlab
figure('Position', [100, 100, 500, 500]);
X = categorical({'#1','#3','#4','#5'});
bar(X,Amean,'LineWidth',0.8 ,'BarWidth',1);
ax = gca;
ax.FontSize = 16; % 字体大小
ax.XGrid = 'on'; % 开启X轴网格
ax.YGrid = 'on'; % 开启Y轴网格
ax.XMinorGrid = 'on'; % 开启X轴次级网格
ax.YMinorGrid = 'on'; % 开启Y轴次级网格
ax.GridColor = [0 0 0]; % 网格颜色
ax.GridAlpha = 0.2; % 网格透明度
ax.MinorGridColor = [0 0 0]; % 次级网格颜色
ax.MinorGridAlpha = 0.2; % 次级网格透明度
ax.LineWidth = 1.0; % 线宽
xlabel("编号");
ylabel("ADU");
title("数据平均值");
```