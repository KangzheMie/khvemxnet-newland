# 🐳 NewLand Docker 部署指南

本目录包含了 NewLand 项目的模块化 Docker 部署脚本，支持分步骤执行和一键部署。

## 📁 文件结构

```
deployment/
├── common.sh              # 通用函数库
├── 01-check-docker.sh      # 步骤1: 检查Docker环境
├── 02-setup-environment.sh # 步骤2: 设置环境变量
├── 03-build-images.sh      # 步骤3: 构建Docker镜像
├── 04-start-services.sh    # 步骤4: 启动服务
├── 05-wait-and-verify.sh   # 步骤5: 等待服务就绪并验证
├── deploy-all.sh           # 一键部署脚本
├── manage-services.sh      # 服务管理脚本
├── docker-compose.yml      # Docker Compose配置
├── Dockerfile.nginx        # Nginx Dockerfile
├── nginx.conf              # Nginx配置
└── README.md               # 本文档
```

## 🚀 快速开始

### 方式一: 一键部署 (推荐)

```bash
# 进入部署目录
cd deployment

# 给脚本添加执行权限
chmod +x *.sh

# 执行一键部署
./deploy-all.sh
```

### 方式二: 分步骤部署

如果某个步骤失败，可以从失败的步骤重新开始，无需从头执行：

```bash
# 进入部署目录
cd deployment

# 给脚本添加执行权限
chmod +x *.sh

# 步骤1: 检查Docker环境
./01-check-docker.sh

# 步骤2: 设置环境变量
./02-setup-environment.sh

# 步骤3: 构建Docker镜像
./03-build-images.sh

# 步骤4: 启动服务
./04-start-services.sh

# 步骤5: 等待服务就绪并验证
./05-wait-and-verify.sh
```

## 🛠️ 服务管理

部署完成后，使用管理脚本进行日常维护：

```bash
# 查看服务状态
./manage-services.sh status

# 查看服务日志
./manage-services.sh logs

# 重启服务
./manage-services.sh restart

# 停止服务
./manage-services.sh stop

# 重新构建并启动
./manage-services.sh rebuild

# 完全清理 (⚠️ 会删除所有数据)
./manage-services.sh clean
```

## 📋 部署步骤详解

### 步骤1: 检查Docker环境
- 验证 Docker 是否安装
- 验证 Docker Compose 是否可用
- 检查 Docker 服务是否运行
- 显示版本信息

### 步骤2: 设置环境变量
- 生成安全密钥
- 创建 `.env` 配置文件
- 配置域名和数据库信息
- 如果 `.env` 已存在，则跳过创建

### 步骤3: 构建Docker镜像
- 拉取基础镜像 (PostgreSQL, Redis)
- 构建自定义应用镜像
- 显示构建结果

### 步骤4: 启动服务
- 停止现有服务
- 启动所有容器
- 显示服务状态

### 步骤5: 等待服务就绪并验证
- 等待数据库启动
- 等待后端服务启动
- 等待前端服务启动
- 显示访问信息和管理命令

## 🌐 访问地址

部署成功后，可以通过以下地址访问：

- **前端**: http://localhost
- **后端API**: http://localhost/api
- **管理后台**: http://localhost/admin

## 🔧 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :80
   netstat -tulpn | grep :1337
   netstat -tulpn | grep :5432
   ```

2. **权限问题**
   ```bash
   # 确保脚本有执行权限
   chmod +x deployment/*.sh
   ```

3. **Docker空间不足**
   ```bash
   # 清理Docker资源
   docker system prune -a
   ```

4. **数据库连接失败**
   - 检查PostgreSQL容器是否正常启动
   - 验证数据库环境变量配置
   - 查看数据库日志：`docker logs newland-postgres`

5. **路径问题**
   - 确保在 `deployment/` 目录下运行脚本
   - 所有相对路径都基于 `deployment/` 目录
   - 前端和后端文件路径使用 `../` 前缀

6. **数据库依赖不匹配**
   - 后端已配置使用PostgreSQL (`pg`包)
   - 确保不要使用SQLite相关配置

### 重新部署

如果需要完全重新部署：

```bash
# 清理所有容器和数据
./manage-services.sh clean

# 重新执行部署
./deploy-all.sh
```

### 仅重新构建应用

如果只是代码更新，无需清理数据：

```bash
# 重新构建并启动
./manage-services.sh rebuild
```

## 📝 环境变量说明

`.env` 文件包含以下重要配置：

```env
# 安全配置 (自动生成)
DB_PASSWORD=...          # 数据库密码
APP_KEYS=...            # 应用密钥
API_TOKEN_SALT=...      # API令牌盐值
ADMIN_JWT_SECRET=...    # 管理员JWT密钥
TRANSFER_TOKEN_SALT=... # 传输令牌盐值
JWT_SECRET=...          # JWT密钥

# 域名配置
DOMAIN=localhost        # 访问域名

# 数据库配置
DATABASE_NAME=newland_db
DATABASE_USERNAME=newland_user

# 环境配置
NODE_ENV=production
TZ=Asia/Shanghai
```

## 🔒 安全注意事项

1. **生产环境部署**
   - 修改默认密码
   - 配置HTTPS证书
   - 限制数据库访问权限
   - 定期备份数据

2. **防火墙配置**
   ```bash
   # 仅开放必要端口
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

3. **数据备份**
   ```bash
   # 备份数据库
   docker exec newland-postgres pg_dump -U newland_user newland_db > backup.sql
   ```

## 🐧 Linux服务器部署

在Linux服务器上部署时的额外注意事项：

1. **系统要求**
   - Ubuntu 20.04+ / CentOS 8+ / Debian 11+
   - Docker 20.10+
   - Docker Compose 2.0+
   - 至少 2GB RAM
   - 至少 10GB 可用磁盘空间

2. **安装Docker**
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # 重新登录或运行
   newgrp docker
   ```

3. **系统服务配置**
   ```bash
   # 设置Docker开机自启
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

## 📞 技术支持

如果遇到问题，请检查：

1. Docker和Docker Compose版本是否符合要求
2. 系统资源是否充足
3. 网络连接是否正常
4. 防火墙设置是否正确

更多信息请参考项目文档或提交Issue。

---

**祝您部署顺利！** 🎉