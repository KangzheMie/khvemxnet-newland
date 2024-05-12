---
title: "Verilog异或"
date: "2024-03-04" # 格式为 YYYY-MM-DD
categories: LoGi
tags:
  - Verilog
summary: "Verilog异或例子"
author: "ChatGPT"
---
# Verilog异或

在 **Verilog** 中，异或运算使用符号 `^` 表示。它是一种基于二进制的位运算，其运算法则是对运算符两侧数的每一个二进制位，**同值取0，异值取1**。简单理解就是**不进位加法**，例如：1 + 1 = 0，0 + 0 = 0，1 + 0 = 1。

以下是一个简单的 **Verilog** 代码示例，用于实现一个 **2 输入异或门**：

```verilog
module xor_gate (
    input a,
    input b,
    output y
);
    assign y = a ^ b;
endmodule
```

在上面的代码中，`a` 和 `b` 是两个输入信号，`y` 是异或门的输出信号。异或门的结果是当两个操作数的值不同时为1，否则为0。
