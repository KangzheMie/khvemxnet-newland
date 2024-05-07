---
title: "Verilog状态机里的计数器"
date: "2024-04-09" # 格式为 YYYY-MM-DD
categories: LoGi
tags:
  - Verilog
summary: "如何把握住状态机"
author: "ChatGPT"
---

# 状态机里的计数器
Verilog的状态机实现一个任务，主要是依靠计数器的计数。

在计数器的不同的数值进行对应的动作，在计数器达到某个值的时候代表一个动作任务的完成，也可以作为状态的转移条件。

### 主任务

``` v
FRAME_TRANS: begin
    if(delay_cnt == ftrans_I2_delay) begin 
        delay_cnt <= delay_cnt;
    end else begin
        delay_cnt <= delay_cnt + 1'b1;
    end

    if(erease_Rcnt == 16'd0) begin
        erease_Rcnt <= erease_Rcnt + 1'b1;
    end else if(erease_Rcnt < ERE_RCNT) begin
        erease_Rcnt <= erease_Rcnt + 1'b1;
    end else begin
        erease_Rcnt <= 16'd0;
    end
end
```

在这个状态中启用了两个定时器来完成一定的逻辑任务, 这两个定时器在时间是同时开始计数的. 对于计数器, 在计数的开始/达到某个值/达到溢出值/达到溢出值之后都可以通过逻辑判断进行一定的动作. 这样只需要把复杂的逻辑过程在时间上分解成较小的步骤, 然后按照计数器不同时刻的指示分布执行, 这样就实际上完成了在一个线性时间上流水化完成一件事情的设计.

上边的程序可以看出这两个任务的特点, delay_cnt是一个一次性任务, 每次只执行一次. 而erease_Rcnt在溢出之后会继续归零, 实际上是一个循环的任务.

### 二级任务

在这个计数器内部, 可能在某个值的时候又启用了一个计数器. 

``` v
if(erease_Rcnt == 16'd0) begin
        erease_Rcnt <= erease_Rcnt + 1'b1;
    end else if(erease_Rcnt < ERE_RCNT) begin
        erease_Rcnt <= erease_Rcnt + 1'b1;
    end else begin
        erease_Rcnt <= 16'd0;

        if(erease_cnt > 28'd0) begin            // 8'd5
            erease_cnt <= erease_cnt - 1'b1;
            charge_dump_flag <=	1'b1;
        end else begin
            line_transfer_flag <= 1'b1;
        end
    end
```

在`erease_Rcnt == ERE_RCNT`开始又启用了一个计数器`erease_cnt`, 发现每次`erease_Rcnt`溢出时计数器`erease_cnt`就会将自己的值减去1.

同时这个计数器会操纵标志位, `xxx_flag`, 然后状态机就会跳转到另一个状态. 所以这个实际上是在完成一个**状态间的循环**任务.

### 释放计数值

在完成任务时「请」保证你的计数器变得干净. 特别是一些计数器会跨状态和任务使用.

``` v
    if(erease_cnt > 28'd0) begin
        frame_transfer_flag	<=	1'b1;
        delay_cnt <= 32'd0;
        time_cntR <= 32'd0;
        time_cntI <= 32'd0;
    end else begin
        exposure_flag <= 1'b1;
        delay_cnt <= 32'd0;
        time_cntR <= 32'd0;
        time_cntI <= 32'd0;
    end 
```

所示的一个计数器在赋值跳转所用的标志位`xxx_flag`之后就顺手把计数器`xxx_cnt`给清零了. 只有清零之后的计数器才能正确的继续使用.


