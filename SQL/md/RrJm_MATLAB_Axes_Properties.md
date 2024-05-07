---
title: "MATLAB Axes Properties"
date: "2024-03-18" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - MATLAB
  - 坐标轴
summary: "MATLAB Axes Properties"
author: "ChatGPT"
---

# Axes Properties

在MATLAB中，Axes Properties是一类非常重要的属性，它们允许您定制和控制坐标轴的外观和行为。您可以通过以下几种方法来设置Axes Properties：

### 1. 使用`set`函数

`set`函数是一种通用方法，可用于设置对象的属性。对于Axes对象，您可以使用它来设置任意属性。例如，要设置坐标轴的标题和标签，可以这样做：

```matlab
ax = gca; % 获取当前坐标轴
set(ax, 'Title', 'My Plot Title', 'XLabel', 'X-Axis Label', 'YLabel', 'Y-Axis Label');
```

### 2. 直接设置属性

在MATLAB中，您可以直接通过Axes对象设置属性。当您创建Axes对象或通过`gca`获取当前Axes对象时，可以直接修改其属性：

```matlab
ax = gca; % 获取当前坐标轴
ax.Title.String = 'My Plot Title';
ax.XLabel.String = 'X-Axis Label';
ax.YLabel.String = 'Y-Axis Label';
```

### 3. 使用图形界面

MATLAB的图形用户界面（GUI）也允许您交互式地修改Axes Properties。通过图形界面，您可以点击并选择特定的坐标轴元素（如标题、轴标签等），并通过属性编辑器直接修改它们。这对于不熟悉编程的用户来说是一个直观的方法。

### 4. 使用`axis`函数

`axis`函数提供了一种快速设置常见Axes属性的方法，例如坐标轴范围和比例。例如，您可以使用它来设置轴的比例为相等，使得一个单位在所有轴上具有相同的长度：

```matlab
axis equal;
```

### 5. 使用特定的函数

MATLAB提供了一系列函数来设置特定的Axes属性。例如，`xlabel`、`ylabel`、`zlabel`和`title`函数可以分别用来设置X轴标签、Y轴标签、Z轴标签和图标题：

```matlab
xlabel('X-Axis Label');
ylabel('Y-Axis Label');
zlabel('Z-Axis Label');
title('My Plot Title');
```



# gca
在 MATLAB 中，`gca` 是一个非常实用的函数，它返回当前图形的坐标轴句柄。通过这个句柄，您可以访问并修改图形的许多属性，以实现对图像的优化和自定义显示。以下是一些常用的参数（属性），您可以通过设置这些参数来优化图像的显示效果：

1. **`XLim`, `YLim`, `ZLim`**：这些属性分别用于设置坐标轴的 X、Y、Z 轴的显示范围。通过调整这些范围，您可以放大或缩小图形的特定部分。

2. **`XLabel`, `YLabel`, `ZLabel`**：这些属性允许您设置坐标轴的标签，以提供关于每个轴代表什么的信息。

3. **`Title`**：用于设置图形的标题。

4. **`XTick`, `YTick`, `ZTick`**：这些属性用于定义坐标轴的刻度位置。

5. **`XTickLabel`, `YTickLabel`, `ZTickLabel`**：通过这些属性，您可以自定义坐标轴刻度的标签。

6. **`FontSize`**：设置坐标轴标签和标题的字体大小。

7. **`GridLineStyle`, `XGrid`, `YGrid`, `ZGrid`**：这些属性用于控制网格线的样式及其是否显示。

8. **`Color`**：设置坐标轴背景色。

9. **`LineWidth`**：定义坐标轴线和坐标轴上刻度线的宽度。

10. **`Box`**：控制是否显示坐标轴周围的边框。

这些只是部分可以通过 `gca` 句柄进行设置的属性。实际上，还有许多其他属性可用于进一步优化和自定义您的图形。要查看所有可用属性及其详细说明，您可以使用 MATLAB 的帮助文档，或通过命令行输入以下命令来获取相关信息：

```matlab
get(gca)
```

此命令会列出当前坐标轴对象的所有属性及其当前值。您也可以使用 `set(gca, 'PropertyName', PropertyValue)` 来修改这些属性，其中 `'PropertyName'` 是您想要修改的属性名称，`PropertyValue` 是您想要设置的新值。



# Example

``` matlab
figure('Position', [100, 100, 1200, 850]);
plot(X1, CH1.mean,'-*', X2, CH2.mean, '-*', X3, CH3.mean, '-*', 'LineWidth',1.1);
ax = gca;
ax.XLim = [0 900];
ax.YLim = [0 700];
ax.FontSize = 14;
ax.XGrid = "on";
ax.YGrid = "on";
ax.XMinorGrid = "on";
ax.YMinorGrid = "on";
ax.GridColor = [0 0 0];
ax.GridAlpha = 0.2;
ax.MinorGridColor = [0 0 0];
ax.MinorGridAlpha = 0.2;
ax.LineWidth = 1.0;
```