## 电脑操作

### windows
F2: 在选择的对象中插入/重命名

Ctrl+R：在MATLAB中批量注释
Ctrl+T：在MATLAB中批量消注释
Ctrl+Shift+N：新建文件夹
Ctrl+Win+o：屏幕键盘
Ctrl+Alt+o：QQ识图

Excel：格式化粘贴中有转置选项

Backspace 键：按下 Backspace 键可以返回上一级文件夹1。
Alt + ←：这个组合键也可以返回上一级文件夹1。

## 命令行
### Linux
Shift + Page Up / Down 上下翻
sudo dpkg -i path 安装.deb
sudo apt-get install -f 安装依赖项

### pandoc
--pdf-engine=xelatex
-V CJKmainfont='SimSun' -V mainfont='Times New Roman'
--highlight-style=breezedark / haddock
--css=blog.css --katex

### git
git config --global http.proxy http://127.0.0.1:xxxxx 设置 HTTP 代理
git config --global https.proxy http://127.0.0.1:xxxxx 设置 HTTPS 代理
git add .
git add * : will only add files that are not hidden
git commit
git push -u origin main
git 在user目录下有.gitconfig 可以移植全局配置

### node.js
npm config get registry
npm config set registry https://registry.npm.taobao.org
npm config set registry https://registry.npmjs.org/

### powershell
Test-NetConnection lodetech.ustc.edu.cn


## 课程资源
### 中科大课程资源
<a href="http://home.ustc.edu.cn/~xhz1995/index.html">计算物理课2019</a>
<a href="http://home.ustc.edu.cn/~zegang/">计算物理课2020</a>
<a href="http://home.ustc.edu.cn/~rzy55555/">计算物理课2021</a>
<a href="http://home.ustc.edu.cn/~lxsphys/index_2022.html">计算物理课2022</a>

<a href="https://blog.csdn.net/DrCube/article/details/78988099">可编程逻辑器件2017试卷</a>
<a href="https://blog.csdn.net/interbvb/article/details/122373267">可编程逻辑器件2021试卷</a>
<a href="https://blog.csdn.net/weixin_43875505/article/details/129205664">可编程逻辑器件2022试卷</a>

<a href="https://blog.csdn.net/li_kin/article/details/103794765">快电子学2019年试卷</a>
<a href="https://www.doc88.com/p-3088954959541.html?r=1">快电子学50题参考答案</a>

### 中科大个人主页
<a href="http://home.ustc.edu.cn/~hr874589148/last/page.html">中科大某学生主页A</a>
<a href="http://home.ustc.edu.cn/~hr874589148/last/test-site/test-paper.html">科大试卷答案下载</a>


## 硬件技巧
### 保护电脑
调试电路板与电脑连接是有反向烧坏电脑的风险的。
特别是对于一些电机类，请使用USB隔离器保护好你的电脑。

### 单片机ROM中的程序是如何参与开机过程的
对于简单的单片机系统（例如STM32等微控制器），通常采取的是部分加载策略。这种策略的关键点包括：

1. **资源优化**：由于单片机的RAM资源有限，部分加载策略有助于优化内存使用，确保系统高效运行。

2. **运行效率**：只将必要的程序和数据加载到RAM中，可以提高系统的运行效率和响应速度。

3. **系统稳定性**：通过精心选择需要加载的程序部分，可以确保系统稳定运行，避免不必要的资源浪费。

这种加载策略适用于大多数简单的嵌入式系统和单片机应用，是在有限资源下实现高效运行的有效方法。


## 可编程逻辑技巧
### verilog
parameter 可以在模块的实例化时被外部模块覆盖，这意味着您可以在模块实例化时为其指定不同的值，从而增加了模块的灵活性。

localparam 则是局部参数，它的值在定义后不能被修改，也就是说它是只读的。

Y <= (X > 4'd9)?(X + 8'd 55 ):(X + 8'd 48); //X是十六进制 Y是ASCII码

reset_project 可以快速清理当前的工程



## 课程规划
### 必修公共        3(9)/9
- MARX6102U         新时代             (2) 
- FORL6101U         研究生综合英语      (2)      
- EIEN6201U         专业英语            (2)
- PHIL6101U         自然辩证法          1
- PHIL6301U         工程伦理            2
  
### 必修数学        0(3)/3
- INFO6101P         矩阵分析            (3)
  
### 必修基础        0(8)/6
- PHYS5256P         计算物理            (4)
- ELEC6103P         近代信息处理        (4)
  
### 选修            8(12)/7
- ELEC5302P         快电子学            3
- ELEC6202P         逻辑设计实验        2
- ELEC6201P         可编程逻辑          3
- ELEC5301P         核电子学            (4)


## 物价记录

香蕉 - 3.5 CNY/500g



