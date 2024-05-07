---
title: "AD电路设计中的标准化"
date: "2024-04-06" # 格式为 YYYY-MM-DD
categories: DmZi
tags:
  - 电子学
  - AD
summary: "一些方便统一管理的小技巧"
author: "KhVeMx"
---

# AD电路设计中的标准化

## 元件名称管理标准化

Designator 指示者，代表元件的指标，如U?

Comment 评价，代表元件的附带说明，如 1uF 25V

管理这部分请使用Tools > parameter manager

![parameter manager](./picture/blog/DmZi_AD电路设计中的标准化_parameterManager.png)

## 元件封装管理标准化

管理这部分请使用Tools > footprint manager

![footprint manager](./picture/blog/DmZi_AD电路设计中的标准化_footprintManager.png)

## 布线宽度标准化

有关阻抗匹配的请查询目标厂家的阻抗计算器

有关电源部分的布线宽度的请使用收藏夹的计算器

## 人性化设计

请注意留有测试点，留有LED指示灯。在投板之前请您首先估计一下所有可能遇到的问题，做一些指示性电路设计。



