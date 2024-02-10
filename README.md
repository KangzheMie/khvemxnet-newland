<p align="center">
<img src="./picture/NewLand.png" width=400px>
</p>
<h2 align="center"> 放在实验室服务器上的小型网页 </h2>
<br/> 

## 介绍

新大陆发现部是利用课题组实验室服务器资源的网页开发练手项目

网站的地址为：http://lodetech.ustc.edu.cn/subpage/wangkangzhe/index.html

## 用途

* 该工程将作为本人练习使用html+css+js+python的实验性项目
* 本网页最终将作为个人放置笔记的仓库使用

## 版本

**2023.11.29**: 
v0.1 第一个稳定运行版本 

**2023.12.06**: 
v0.2 增加了子菜单功能, 让日志可以在子菜单页面上显示 

**2023.12.09**: 
v0.3 新增blog模块。使用[pandoc](https://github.com/jgm/pandoc)转换md文件到html，使用[KaTeX](https://github.com/KaTeX/KaTeX)和[HighLight.js](https://github.com/highlightjs/highlight.js)库对blog文章中的公式和代码渲染。

**2023.12.20**: 
v0.4 新增手机适配；重新排版所有页面；继续开发新的栏目

**2024.02.10**：
v1.0 Happy Loong Year；
- 架构大更新 将静态网页的各个部分分别使用js脚本动态加载；
- 新增 <span style="color: #ffcfe0;">「Elysia」</span>主题包；
- 新增 自动化发布blog/log的python脚本
- 优化 blog/log导航界面样式
- 优化 超长数学公式在手机上的显示
- 修改 首页欢迎界面