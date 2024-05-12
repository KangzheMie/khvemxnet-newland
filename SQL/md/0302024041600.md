---
title: "Linux搭建LNMP"
date: "2024-04-16" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - Linux
  - 命令行
summary: "Linux搭建LNMP"
author: "ChatGPT"
---

# Linux搭建LNMP

在Ubuntu系统上搭建LNMP（Linux, Nginx, MySQL, PHP）网站服务器。

### 第一步：系统更新

在开始之前，确保的Ubuntu系统是最新的。这可以通过运行以下命令来完成：

```bash
sudo apt update && sudo apt upgrade -y
```

这将确保所有已安装的软件包是最新的，并且系统没有已知的安全漏洞。

### 第二步：安装Nginx

Nginx是一种高性能的Web服务器软件，它也可以作为反向代理服务器和负载均衡器使用。安装Nginx可以通过以下命令完成：

```bash
sudo apt install nginx -y
```

安装完成后，可以通过运行以下命令来检查Nginx服务的状态：

```bash
systemctl status nginx
```

如果服务正在运行，可以在Web浏览器中输入服务器的IP地址来测试Nginx服务器是否正常工作。应该能看到Nginx的默认欢迎页面。

### 第三步：安装MySQL

MySQL是一个广泛使用的关系型数据库管理系统。在Ubuntu上安装MySQL，可以使用以下命令：

```bash
sudo apt install mysql-server -y
```

安装完成后，应运行一个安全脚本来改善MySQL数据库的安全性：

```bash
sudo mysql_secure_installation
```

按照提示进行操作，设置root用户密码，移除匿名用户，禁止root用户远程访问，并删除测试数据库。

### 第四步：安装PHP

PHP是一种广泛使用的开放源代码脚本语言，尤其适用于Web开发并可以嵌入到HTML中。安装PHP及其与Nginx配合使用的必要模块：

```bash
sudo apt install php-fpm php-mysql -y
```

安装完毕后，需要进行少量配置，使PHP与Nginx配合工作。打开默认的Nginx配置文件：

```bash
sudo nano /etc/nginx/sites-available/default
```

确保的配置文件中有以下部分来处理PHP请求：

```bash
location ~ \.php$ {
    include snippets/fastcgi-php.conf;
    fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;  # 注意PHP版本号可能需要调整
    fastcgi_index index.php;
    include fastcgi_params;
}
```

完成后，重启Nginx以应用更改：

```bash
sudo systemctl restart nginx
```

### 第五步：测试PHP

创建一个PHP文件来测试PHP是否正常工作：

```bash
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php
```

然后在Web浏览器中输入 `http://your_server_ip/info.php`。应该能看到PHP的配置和版本信息。
