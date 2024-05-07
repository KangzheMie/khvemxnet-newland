---
title: "Verilog SDC约束文件的写法"
date: "2024-03-04" # 格式为 YYYY-MM-DD
categories: LoGi
tags:
  - AI
  - Verilog
summary: "SDC约束文件的写法"
author: "ChatGPT"
---

# Verilog SDC约束文件的写法

## 约束时钟

如果您的工程输入时钟是50MHz，并且使用PLL内部产生了200MHz和20MHz的时钟，而且没有特定的输入输出延迟要求，SDC（Synopsys Design Constraints）文件的编写可以相对简单。以下是一个基本的SDC文件编写示例，展示如何为这些时钟定义时序约束：

```tcl
# 定义输入时钟
create_clock -name clk_in -period 20.0 [get_ports {input_clk_port_name}]
# 50MHz时钟周期为20ns

# 定义PLL产生的时钟
# 假设PLL的输出时钟分别连接到了某些内部信号上
create_generated_clock -name clk_200M -source [get_ports {input_clk_port_name}] -multiply_by 4 [get_pins {pll_instance_name/output_clk_200M}]
# PLL将50MHz时钟倍频到200MHz，周期为5ns

create_generated_clock -name clk_20M -source [get_ports {input_clk_port_name}] -divide_by 2.5 [get_pins {pll_instance_name/output_clk_20M}]
# PLL将50MHz时钟分频到20MHz，周期为50ns

# 由于没有输入输出延迟的特定要求，以下两行是可选的
# 这里假设默认的输入输出延迟约束对于设计来说是可接受的
# set_input_delay 0 -clock clk_in [all_inputs]
# set_output_delay 0 -clock clk_in [all_outputs]

# 如果您的设计中有特定路径不需要时序分析，可以使用如下命令来设置
# set_false_path -from [get_clocks clk_in] -to [get_clocks clk_200M]
# set_false_path -from [get_clocks clk_in] -to [get_clocks clk_20M]

```

在这个示例中，我们首先定义了50MHz的输入时钟，然后根据您的描述，使用create_generated_clock命令定义了由PLL产生的200MHz和20MHz时钟。在这些命令中，-source参数指定了时钟源，-multiply_by和-divide_by参数分别用于定义时钟频率的倍增和分频。

请注意，{input_clk_port_name}、{pll_instance_name/output_clk_200M}、和{pll_instance_name/output_clk_20M}需要根据您的实际设计中的端口名和实例名进行替换。

如果您的设计中确实没有输入输出延迟的要求，那么可以不用添加set_input_delay和set_output_delay命令。但是，如果您希望明确指出没有延迟，可以将这些命令的延迟值设置为0。


根据您的描述，如果您的20MHz时钟是通过将25MHz的输入时钟倍频40倍后，再分频50得到的，那么您需要相应地调整create_generated_clock命令中的-multiply_by和-divide_by参数来反映这一点。这里是如何为该20MHz输出时钟添加约束的步骤：

### 定义输出时钟

使用create_generated_clock命令为20MHz输出时钟定义约束。考虑到您的MMCM配置，您需要指定倍频和分频的值。假设clk_out1是20MHz时钟输出，您可以这样写：

```tcl
create_generated_clock -name clk_20 -source [get_ports {CLK_25_IN}] -multiply_by 40 -divide_by 50 [get_pins {clk_wiz_0/clk_wiz_0_u0/clk_out1}]
```

这里，-multiply_by 40和-divide_by 50参数精确地描述了从25MHz输入时钟到20MHz输出时钟的转换过程。-source参数指明了该时钟的来源，即25MHz的输入时钟。

### 确认约束正确性

在添加任何约束之前，非常重要的一点是确认这些约束是否反映了您的设计意图和MMCM的配置。对于倍频和分频的计算，确保它们的组合能够产生您期望的输出时钟频率。在本例中，25MHz乘以40再除以50确实得到20MHz，这意味着您的约束设置是正确的。

### 其他注意事项

- 确保您的MMCM配置（如倍频和分频值）与实际硬件设计和需求相匹配。
- 使用Vivado时，请参考最新的官方文档，以获取关于如何正确设置时钟约束的最新信息和最佳实践。
- 在设计流程中，适时地进行时序分析，确保满足所有时序要求。

## 约束引脚

Verilog约束文件中的两种形式，它们的目的是相同的——都用于配置FPGA引脚的属性，包括指定特定的引脚和电压标准。然而，这两种形式在语法和可读性方面存在一些差异。我将对这两种形式进行详细解析，以帮助您更好地理解它们的相同点和不同点。

### 第一种形式：使用 -dict 选项

```verilog
set_property -dict {PACKAGE_PIN AC9 IOSTANDARD LVDS} [get_ports Pulse1_p]
set_property -dict {PACKAGE_PIN AD9 IOSTANDARD LVDS} [get_ports Pulse1_n]
```

这种形式通过使用 -dict 选项，允许您在一条命令中设置多个属性。这里，PACKAGE_PIN 和 IOSTANDARD 是被设置的两个属性，分别指定了引脚位置和I/O标准（如LVDS）。[get_ports Pulse1_p] 和 [get_ports Pulse1_n] 分别指定了要配置的端口名。

### 第二种形式：逐个设置属性

```verilog
set_property PACKAGE_PIN V11 [get_ports {FPGA_RF_OUT_CH[1]}]
set_property IOSTANDARD LVCMOS18 [get_ports {FPGA_RF_OUT_CH[1]}]
```

在这种形式中，每个 set_property 命令单独设置一个属性。第一行命令设置了引脚位置（PACKAGE_PIN），而第二行命令设置了I/O标准（IOSTANDARD）。这两行命令共同配置了同一个端口的两个属性。

### 相同点与不同点

**相同点：**
- 两种形式都用于配置FPGA引脚的属性，包括引脚位置和I/O标准。
- 都需要指定端口名。

**不同点：**
- **语法与可读性：** 第一种形式使用 -dict 选项在一条命令中同时设置多个属性，这可以使约束文件更加简洁。而第二种形式逐个属性设置，可能使得配置过程更加明确和可读，特别是对于初学者而言。
- **灵活性：** -dict 形式在处理多个属性时可能更加高效，但如果您只需要设置单一属性，两种方法都很适用。

总的来说，选择哪种形式主要取决于个人偏好和项目需求。如果需要简洁的代码，或者同时设置多个属性，使用 -dict 形式可能更优。如果注重代码的可读性，或者逐步调试和验证每个属性，逐个设置属性可能更合适。


## 假路径（用于忽略路径上的约束）

命令：

```verilog
set_false_path -from [get_pins u_generate_pulse_top/u1_clk_wiz_1/inst/mmcm_adv_inst/CLKOUT0] -to [get_pins {u_generate_pulse_top/u1_div_pulse/pulse_in_reg_reg[0]/D}]
```

这是在使用时序约束中的一个非常重要的命令，用于指定FPGA设计中的一个“假路径”(false path)。在数字电路设计和时序分析中，假路径是指那些不需要遵循严格时序要求的路径。这意味着，时序分析器在进行时序检查时，会忽略这些路径上的时序要求。这通常用于那些不会影响实际功能或性能的路径，或者是由于设计特点确实不可能满足时序要求的路径。

**解析该命令的各部分：**

- set_false_path：这是设置假路径的命令，告诉时序分析器忽略从特定源到特定目的地的路径。
- -from [get_pins ...]：指定假路径的起点，这里是u_generate_pulse_top/u1_clk_wiz_1/inst/mmcm_adv_inst/CLKOUT0引脚。这通常是一个时钟输出引脚，表示从这个时钟输出开始的路径。
- -to [get_pins ...]：指定假路径的终点，这里是u_generate_pulse_top/u1_div_pulse/pulse_in_reg_reg[0]/D引脚。这通常是一个数据或控制信号的输入引脚，表示路径终止于这个点。

**为什么要设置假路径？**

- **优化设计：**通过指定假路径，可以让时序分析器忽略那些不影响整体性能的路径，从而专注于优化那些真正重要的时序路径。
- **解决时序问题：**在某些情况下，特定路径可能由于设计上的特殊考虑，其实并不需要满足严格的时序要求。通过标记这些路径为假路径，可以避免时序分析器报告不必要的时序违规。
- **增强灵活性：**设计师可以根据实际设计的需要，有选择性地忽略某些路径的时序要求，这为复杂设计的时序优化提供了更大的灵活性。

综上所述，set_false_path命令是时序约束设计中非常重要的一部分，它帮助设计师精确控制时序分析的范围和焦点，从而优化整个设计的性能和稳定性。