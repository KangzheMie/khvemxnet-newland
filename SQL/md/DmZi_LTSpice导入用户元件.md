---
title: "LTSpice导入用户元件"
date: "2024-04-28" # 格式为 YYYY-MM-DD
categories: DmZi
tags:
  - 电子学
  - 电路仿真
summary: "LTSpice导入用户元件"
author: "KhVeMx"
---

# LTSpice导入用户元件

LTSpice导入电路元件模型以Spice文件为基础。

## Spice文件

### Spice文件的组成

对于一个复杂的自定义电路模块，是以.subckt开头的，意思是子电路（sub-circuit）。例如在in和out节点之间定义一个RC并联电路。
``` verilog
.subckt myamplifier in out
R1 in out 1k
C1 in out 10u
.ends
```

此外还可以给特定类型的元件，比如二极管，赋予物理参数来定义用户模型。使用.model命令，例如定义用户特定参数的PNP二极管。
``` verilog
.model Mypnp PNP (Is=6.734f Xti=3 Eg=1.11 
+ Vaf=74.03 Bf=416.4 Ne=1.259 Ise=6.734f 
+ Ikf=66.78m Xtb=1.5 Br=10.61 Nc=2 Isc=0)
```

### LM358 Spice文件解析
``` verilog
.subckt LMX58_LM2904 IN+ IN- VCC VEE OUT
******************************************************
* MODEL DEFINITIONS:
.model BB_SW VSWITCH(Ron=50 Roff=1e12 Von=700e-3 Voff=0)
.model ESD_SW VSWITCH(Ron=50 Roff=1e12 Von=250e-3 Voff=0)
.model OL_SW VSWITCH(Ron=1e-3 Roff=1e9 Von=900e-3 Voff=800e-3)
.model OR_SW VSWITCH(Ron=10e-3 Roff=1e9 Von=1e-3 Voff=0)
.model R_NOISELESS RES(T_ABS=-273.15)
******************************************************


I_OS        ESDn MID -18N
I_B         37 MID -20N
V_GRp       57 MID 180
V_GRn       58 MID -180
V_ISCp      51 MID 40
.........
```

首先声明了对外的接口
```verilog
.subckt LMX58_LM2904 IN+ IN- VCC VEE OUT
```

然后为自己的模型定制特定参数的模型，比如定义了一个R_NOISELESS电阻，他具有参数T_ABS=-273.15。
```verilog
.model R_NOISELESS RES(T_ABS=-273.15)
```

之后开始对各种器件连线
``` verilog
[元件_名] [节点1] [节点2] ... [值]
```


## Spice文件的导入

### 从外界导入
在LTSpice中使用如下的spice命令可以把外部的文件导入到工程之中

在Edit > SPICE Directive中

``` verilog
.lib "standard.mos"  ; 导入标准MOSFET模型库
.include "mycircuit.cir"  ; 引入包含整个电路的SPICE文件
```

命令之后的路径可以使用相对路径，所以外部的文件可以直接存储在电路仿真工程的文件下。

### 内嵌到文件中

使用Edit > SPICE Directive， 然后把spice文本写入到其中。此时LTSpice的这个工程就可以直接通过使用`ModuleName`的元件来使用spice模型。
![LTSpice元件内嵌](./picture/blog/DmZi_LTSpice元件内嵌.png)

### 自动生成器件符号
把导入的文件在LTSpice中打开，然后在对外接口的文本位置右键，即可发现自动生成器件符号的选项。

### 关联已有器件符号
比如一个三极管模型NPN，可以把三极管的名字更改为用户导入模型中的`ModuleName`，LTSpice会自动关联三极管模型和导入的Spice模型。

### 对于来自不同厂商的模型的处理
不同厂商的库，实际上内部的基本语法都是spice，而对外的接口被各自改造了。

LTspice的对外接口模式为
``` verilog
.subckt ModuleName Prot1 Prot2
```

或者

``` verilog
.model ModuleName ModelName(params)
```

实际上只需要把别的厂商的库中的接口改成LTSpice的标准即可。
