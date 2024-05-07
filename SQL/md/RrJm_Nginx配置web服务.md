---
title: "Nginx配置web服务"
date: "2024-04-17" # 格式为 YYYY-MM-DD
categories: RrJm
tags:
  - Linux
  - 命令行
summary: "Nginx配置web服务"
author: "ChatGPT"
---

# Nginx配置web服务
## Nginx的工作逻辑

1. **配置文件设置**：Nginx 通过配置文件来设定其运行参数和管理各种服务的设置。配置文件通常位于 `/etc/nginx/nginx.conf` 和 `/etc/nginx/sites-available/` 目录下的文件中。这些文件定义了Nginx 如何处理进入的网络请求，包括监听的端口、处理请求的服务器、URL 路由规则等。

2. **服务器块 (Server Blocks)**：这些是在 Nginx 配置中定义的，相当于 Apache 的虚拟主机。服务器块允许您为不同的域名、端口或IP地址配置不同的Web页面和应用程序。例如，您可以设置一个服务器块来处理在端口 80 上接收的请求，而另一个处理在端口 81 上的请求。

3. **文档根目录 (Document Root)**：每个服务器块会指定一个文档根目录，这是服务器上存储网页文件（如 HTML 文件）的目录。当用户请求一个网页时，Nginx 会从这个目录查找和提供文件。

4. **用户权限**：为了确保Nginx能够访问这些文件，通常需要将网页文件的所有权和权限设置为 Nginx 运行用户（通常是 `www-data`）。这确保了Nginx 能够读取和提供存储在文档根目录中的文件。

5. **监听请求**：配置文件中的 `listen` 指令告诉 Nginx 监听哪个端口（如 80, 443 等）。每当有请求到达这些端口时，Nginx 就会根据配置处理这些请求，例如，返回一个静态页面或将请求转发到后端服务器。

6. **处理请求**：Nginx 使用 `location` 块来决定如何处理特定的路径和请求。例如，它可以直接从文件系统中提供静态文件，或者通过 FastCGI 协议将请求传递给后端的 PHP 处理器。

## Nginx的配置文件
``` py
server {
    listen 80;                    # 监听80端口
    server_name your_domain.com;  # 域名/服务器IP

    root /var/www/html/port80;    # root命令:指定文档根目录
    index index.html;             # index命令:默认索引文件

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;  # 注意PHP版本号可能需要调整
        fastcgi_index index.php;
        include fastcgi_params;
    }
}
```
其中

```py
location / {
    try_files $uri $uri/ =404;
}
```

这个配置段的作用是定义了对根 URL（即 `/`）的请求如何处理。它使用 `try_files` 指令来尝试依次找到并返回请求的文件。

```py
location ~ \.php$ {
    include snippets/fastcgi-php.conf;
    fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;  # 注意PHP版本号可能需要调整
    fastcgi_index index.php;
    include fastcgi_params;
}
```

这个配置段处理以 `.php` 结尾的请求，它用于设置 PHP 文件的处理方式。


## 设置网页服务的步骤

### 第一步：准备文件和目录

首先，为每组网页创建并准备好目录和文件。例如：

```bash
sudo mkdir -p /var/www/html/port80
sudo mkdir -p /var/www/html/port81

sudo cp /path/to/your/index80.html /var/www/html/port80/index.html
sudo cp /path/to/your/index81.html /var/www/html/port81/index.html
```

确保将 `/path/to/your/index80.html` 和 `/path/to/your/index81.html` 替换为实际的文件路径。

其中默认路径可以在Nginx配置中使用`root`命令更改为指定的路径。

### 第二步：设置权限

确保Nginx用户可以访问这些目录和文件：

```bash
sudo chown -R www-data:www-data /var/www/html/port80
sudo chown -R www-data:www-data /var/www/html/port81

sudo chmod -R 755 /var/www/html/port80
sudo chmod -R 755 /var/www/html/port81
```

将网页文件的所有权和权限设置为 Nginx 运行用户（通常是 `www-data`）

### 第三步：配置Nginx

编辑Nginx的配置文件来添加两个服务器块，每个都监听不同的端口：

打开Nginx的配置文件：

```bash
sudo nano /etc/nginx/sites-available/default
```

添加或修改两个 `server` 块如下：

```py
server {
    listen 80;  # 监听80端口
    server_name your_domain.com;  # 或您的服务器IP

    root /var/www/html/port80;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 81;  # 监听81端口
    server_name your_domain.com;  # 或您的服务器IP

    root /var/www/html/port81;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

这里每个 `server` 块配置了不同的 `root` 指令以指向不同的目录。

### 第四步：重启Nginx

保存配置并退出编辑器，然后重启Nginx来应用更改：

```bash
sudo systemctl restart nginx
```

### 第五步：测试访问

在Web浏览器中分别访问：

- `http://your_server_ip/` 会访问端口80上的网页。
- `http://your_server_ip:81/` 会访问端口81上的网页。
