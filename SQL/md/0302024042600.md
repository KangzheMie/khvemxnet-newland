---
title: "PHP实现网站访问计数"
date: "2024-04-26" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - Linux
  - PHP
summary: "PHP实现网站访问计数"
author: "ChatGPT"
---

# PHP实现网站访问计数

## PHP脚本
``` php
<?php
$interview_log_file = 'interview_log.txt';  // 定义日志文件名
$counter_file = 'counter.txt';              // 定义存放访问次数的文件名
$time = date('Y-m-d H:i:s');                // 获取当前时间字符串

// 检查并更新访问次数
if (!file_exists($counter_file)) {
    $counter = 1;
    file_put_contents($counter_file, $counter);
} else {
    $counter = (int)file_get_contents($counter_file) + 1;
    file_put_contents($counter_file, $counter);
}

// 检查日志文件是否存在，若不存在则创建
if (!file_exists($interview_log_file)) {
    file_put_contents($interview_log_file, "counter : Time\n");  
}

// 将访问次数和时间记录到日志文件
$log_entry = $counter . ' : ' . $time . "\n";
// 使用FILE_APPEND标志来追加数据
file_put_contents($interview_log_file, $log_entry, FILE_APPEND);  

echo $counter;
?>
```

PHP（全称为 "PHP: Hypertext Preprocessor"，即“超文本预处理器”）是一种广泛用于服务器端编程的脚本语言。PHP最初被设计用来创建动态网页内容，它可以在服务器上执行，生成HTML，然后发送给客户端的浏览器显示。

- PHP代码通常在Web服务器上执行，而不是在客户端浏览器上执行。这意味着PHP可以执行如访问数据库、文件操作、网络请求等服务器级任务。
- PHP可以直接嵌入到HTML代码中，使用 <?php ... ?> 标签。可以直接在HTML文件中插入PHP代码来输出动态内容。

### 注意事项
对目标的目录配置好php环境
``` php
server {
    listen 80;
    server_name example.com;  

    root /var/www/html;  # 网站的根目录
    index index.php index.html index.htm;

    # 处理 PHP 脚本的位置指令
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;

        # 对于 socket 方式:
        # fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
    }

    # 处理静态文件，直接返回静态内容，不通过 PHP 处理
    location / {
        try_files $uri $uri/ =404;
    }
}
```

然后重启nginx服务
```bash
sudo systemctl restart nginx
```

确保PHP环境对所操作的目录有写权限，否则 `file_put_contents()` 函数可能因权限问题失败。

``` bash
chmod 666 counter.txt
```

## HTML部分
``` html
<div class="visitor-wrapper">
    <p>访问次数：</p><div id="visitorCount">正在加载访客数...</div>
</div>
```

``` css
.visitor-wrapper {
    display: flex; /* 使用flex布局使子元素排列在同一行 */
    align-items: center; /* 垂直居中对齐子元素 */
    justify-content: center; /* 水平居中对齐子元素 */
}

#visitorCount {
    display: inline; /* 将div设置为行内元素 */
}
```
`<p>`和`<div id = "visitorCount">`在父级标签`<div class = "visitor-wrapper">`下水平垂直对齐。

``` js
document.addEventListener('DOMContentLoaded', function() {
    // 创建一个新的AJAX请求
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'counter.php'); // 指定请求的类型和URL
    xhr.onload = function() {
        if (xhr.status === 200) {
            // 请求成功，将返回的文本设置到div中
            document.getElementById('visitorCount').innerText = xhr.responseText;
        } else {
            // 出错时的处理
            document.getElementById('visitorCount').innerText = "???";
        }
    };
    xhr.send(); // 发送请求
})
```

在同步执行阶段，`xhr.onload`注册了加载事件之后的回调函数，然后通过`xhr.send()`将php脚本发送到浏览器执行。

当php加载完毕后，把返回的文本`echo $counter;`写入ID为`'visitorCount'`的文本中。

### 注意事项
js脚本加载的时机很重要，如果在`'visitorCount'`尚未加载的时候执行上述脚本，将会报错「找不到getElementById」。

确保JavaScript代码在相关的DOM元素加载完成之后执行。可以在紧贴着`</body>`的前面放置`<script>`。