---
title: "Vivado综合实现电路实例"
date: "2024-04-05" # 格式为 YYYY-MM-DD
categories: LoGi
tags:
  - 可编程逻辑器件
summary: "vivado对于RTL电路是如何综合和实现的"
author: "KhVeMx"
---

# Vivado综合实现电路实例

## RTL Analysis
拿一个2输入的与门做例子

``` verilog
assign Z = X & Y;

set_property -dict {PACKAGE_PIN F24  IOSTANDARD LVCMOS18} [get_ports X]
set_property -dict {PACKAGE_PIN AF24 IOSTANDARD LVCMOS18} [get_ports Y]
set_property -dict {PACKAGE_PIN L21  IOSTANDARD LVCMOS18} [get_ports Z]
```

![RTL分析得到的电路](./picture/blog/RrJm_Vivado综合实现电路实例_RTL.png)

## Synthesis
经过综合之后，按照上述的RTL逻辑所需，并且结合目前工程的芯片情况，会生成一份「网表(Netlist)文件」。

这一份文件描述的是，完成RTL逻辑需要哪些具体的叶单元(Leaf Cell)和连线(Net)。

![综合网表得到的电路](./picture/blog/RrJm_Vivado综合实现电路实例_synthesis.png)

如上图所示的是，完成一个与门，需要使用：

- 2个 IBUF 输入缓冲器
- 1个 OBUF 输出缓冲器
- 1个 LUT  查找表

有了这些树的枝叶和连线的信息，他们就可以完整的描述一个逻辑电路的「拓扑关系」。

理想情况下，只要满足这样拓扑的电路都可以实现RTL的逻辑需求。

### 网表文件长什么样

File -> Export -> Export Netlist

EDIF (Electronic Design Interchange Format)是一种基于 S 表达式的供应商中立格式，用于存储电子网表和原理图。这是为电子设计自动化 (EDA) 行业建立中立数据交换格式的首批尝试之一。目标是建立一种通用格式，从中可以派生出 EDA 系统的专有格式。

``` verilog
(edif demo
  (edifversion 2 0 0)
  (edifLevel 0)
  (keywordmap (keywordlevel 0))
(status
 (written
  (timeStamp 2024 04 05 20 47 35)
  (program "Vivado" (version "2019.2"))
  (comment "Built on 'Wed Nov  6 21:40:23 MST 2019'")
  (comment "Built by 'xbuild'")
 )
)
  (Library hdi_primitives
    (edifLevel 0)
    (technology (numberDefinition ))
   (cell IBUF (celltype GENERIC)
     (view netlist (viewtype NETLIST)
       (interface 
        (port O (direction OUTPUT))
        (port I (direction INPUT))
       )
     )
   )

   ...

   (Library work
    (edifLevel 0)
    (technology (numberDefinition ))
   (cell demo (celltype GENERIC)
     (view demo (viewtype NETLIST)
       (interface 
        (port X (direction INPUT))
        (port Y (direction INPUT))
        (port Z (direction OUTPUT))
       )
       (contents
         (instance X_IBUF_inst (viewref netlist (cellref IBUF (libraryref hdi_primitives))))
         (instance Y_IBUF_inst (viewref netlist (cellref IBUF (libraryref hdi_primitives))))
         (instance Z_OBUF_inst (viewref netlist (cellref OBUF (libraryref hdi_primitives))))
         (instance Z_OBUF_inst_i_1 (viewref netlist (cellref LUT2 (libraryref hdi_primitives)))
           (property INIT (string "4'h8"))
         )
         (net X (joined
          (portref I (instanceref X_IBUF_inst))
          (portref X)
          )

           (property IOSTANDARD (string "LVCMOS18"))
         )
    ...
```

verilog 版本：

``` verilog
input X;
input Y;
output Z;

wire X;
wire X_IBUF;
wire Y;
wire Y_IBUF;
wire Z;
wire Z_OBUF;

IBUF X_IBUF_inst
      (.I(X),
      .O(X_IBUF));
IBUF Y_IBUF_inst
      (.I(Y),
      .O(Y_IBUF));
OBUF Z_OBUF_inst
      (.I(Z_OBUF),
      .O(Z));
LUT2 #(
  .INIT(4'h8)) 
  Z_OBUF_inst_i_1
      (.I0(X_IBUF),
      .I1(Y_IBUF),
      .O(Z_OBUF));
```

## Implementation

网表文件的格式只约束了各个逻辑单元Cell的拓扑关系，没有在空间时间上具有约束。

空间上，芯片内部的连线资源各不相同，并且需要满足IO引脚的空间约束。

时间上，连线需要满足各种时序尽可能延迟短并且同时，并且需要满足用户定义的各种时序约束。

本工程中没有多余的约束，所以系统会按照最短延迟来布线。

![布线整体视图](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation1.png)

下图展示了抽象的LUT

![LUT](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation2.png)

下图展示了比较具体的LUT附近的连线过程

![具体的LUT附近的连线过程](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation3.png)

从上图的展示可以发现，连线是一个复杂的过程。从IO到所指定的查找表并不是直接连线，而是经过了多层的路由转接。

### 探究逻辑单元和连线单元的样子
![连线单元和逻辑单元](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation4.png)

从上图可以看出来两个主要的结构：一是负责桥接连线的单元，二是负责逻辑处理的单元。

他们大概每四个一组

![连线单元和逻辑单元](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation5.png)

![连线单元和逻辑单元](./picture/blog/RrJm_Vivado综合实现电路实例_Implementation6.png)