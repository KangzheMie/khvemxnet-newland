---
title: "Verilog状态机三段式"
date: "2024-04-10" # 格式为 YYYY-MM-DD
categories: LoGi
tags:
  - Verilog
summary: "Verilog状态机三段式"
author: "KhVeMx"
---
# Verilog状态机三段式

``` v
localparam S1 = 2'b00;  //state examples
localparam S2 = 2'b01;
localparam S3 = 2'b11;
localparam S4 = 2'b10;

reg [1:0] cstate; //current state from next state in synchronous
reg [1:0] nstate; //next state form Combinational logic

reg reg1,reg2,reg3; //register examples


//Synchronous state machine
always @(posedge clk or negedge rst_n) begin
	if(!rst_n) begin
		cstate <= S1;
	end else begin
		cstate <= nstate;
	end
end 

//Asynchronous Combinational logic circuit for states' transforming
//Point: in Combinational logic circuit YOU SHOULD USE "=" instead of "<="
always @(*) begin
    if(!rst_n)
        nstate = S1;
    else begin
        case(cstate)
            S1: begin
                if(condition1) nstate = S2;
                else nstate = S1;
            end
            S2: begin
                if(condition2) nstate = S3;
                else if(condition3) nstate = S1;
                else nstate = S2;
            end
            S3: ...
            S4: ... 
            default: nstate = S1;
        endcase
    end
end

//Synchronuos logic circuit
//Registers behavior and some synchronous outputs registers
//In synchronous circuit you should use "<=" for registers
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        reg1 <= 0;
        reg2 <= 0;
        reg3 <= 0; // you should synchronous reset all registers
    end else begin
        case(nstate)
            S1: begin
                reg1 <= XXX;
                if(condition1) reg2 <= XXX;
                condition1 <= 1;
            end
            S2: begin
                reg3 <= XXX;
            end
            S3:
            S4:
            default:
        endcase
    end
end

```

