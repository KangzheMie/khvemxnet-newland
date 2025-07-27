# 🐳 NewLand Docker 部署指南

本目录包含了 NewLand 项目的智能化 Docker 部署脚本，支持分步骤执行和一键部署，具备网络自适应构建能力。

## 📁 文件结构

```
deployment/
├── common.sh               # 通用函数库 (包含智能网络检测)
├── 01-check-docker.sh      # 步骤1: 检查Docker环境
├── 02-setup-environment.sh # 步骤2: 设置环境变量 + 网络检测
├── 03-build-images.sh      # 步骤3: 构建Docker镜像 (统一入口)
├── 03a-pull-base-images.sh # 步骤3a: 拉取基础镜像
├── 03b-build-backend.sh    # 步骤3b: 智能构建后端镜像
├── 03c-build-nginx.sh      # 步骤3c: 构建前端镜像
├── 04-start-services.sh    # 步骤4: 启动服务
├── 05-wait-and-verify.sh   # 步骤5: 等待服务就绪并验证
├── 06-verify-admin-panel.sh # 步骤6: 验证和修复管理面板
├── 07-data-import.sh       # 数据导入工具
├── deploy-all.sh           # 一键部署脚本
├── manage-services.sh      # 服务管理脚本
├── diagnose-network.sh     # 网络诊断工具
├── docker-compose.yml      # Docker Compose配置
├── Dockerfile.nginx        # Nginx Dockerfile
├── nginx.conf              # Nginx配置
├── DATA_IMPORT_GUIDE.md    # 数据导入详细指南
└── README.md               # 本文档
```

## 🌟 新特性

### 🧠 智能网络自适应构建
- **自动网络检测**: 在环境设置阶段自动检测网络质量
- **智能Dockerfile选择**: 根据网络状况自动选择最适合的构建配置
  - 网络良好 (≥75%): 使用完整版 `backend/Dockerfile`
  - 网络一般 (≥50%): 使用优化版 `backend/Dockerfile`
  - 网络较差 (<50%): 使用轻量级 `backend/Dockerfile.lite`
- **构建优化**: 自动配置国内镜像源，提高构建成功率
- **重试机制**: 构建失败时自动重试，包含缓存清理和故障排除建议

### 🎛️ 管理面板自动化
- **自动构建验证**: Dockerfile 中包含管理面板构建和验证步骤
- **智能修复**: `./06-verify-admin-panel.sh` 自动检测和修复管理面板问题
- **部署后验证**: 部署完成后自动验证管理面板可用性
- **一键修复**: 如果管理面板异常，提供自动修复功能

### 📊 数据导入工具
- **数据库内容自动导入**: 支持批量导入数据库记录
- **文件内容批量导入**: 支持上传和导入各种文件类型
- **导入状态验证**: 实时监控导入进度和状态
- **详细的导入指南**: 提供完整的数据导入操作文档

### 🔧 增强的故障排除
- **网络诊断工具**: `./diagnose-network.sh` 提供详细的网络连接诊断
- **智能错误处理**: 根据网络状况提供针对性的解决建议
- **构建日志优化**: 更清晰的构建过程反馈和错误信息

## 🚀 快速开始

### 一键部署 (推荐)

```bash
# 进入部署目录
cd deployment/

# 一键部署 (包含智能网络检测和优化)
./deploy-all.sh
```

**智能化特性**:
- 🌐 **自动网络检测**: 在部署开始时检测网络质量
- 🎯 **智能Dockerfile选择**: 根据网络状况自动选择最优构建方式
- 🔄 **自动重试机制**: 构建失败时自动重试，提高成功率
- 📊 **实时进度反馈**: 详细的构建进度和状态信息
- 🛠️ **智能故障排除**: 提供针对性的错误解决建议

### 分步骤部署

如果需要更细粒度的控制：

```bash
# 1. 检查Docker环境
./01-check-docker.sh

# 2. 设置环境变量 + 网络检测
./02-setup-environment.sh

# 3. 构建Docker镜像 (智能化)
./03-build-images.sh

# 4. 启动服务
./04-start-services.sh

# 5. 等待服务就绪并验证
./05-wait-and-verify.sh

# 6. 验证管理面板 (可选，通常在步骤5中自动执行)
./06-verify-admin-panel.sh

# 7. 数据导入 (可选)
./07-data-import.sh
```

### 网络诊断 (可选)

如果遇到网络相关问题：

```bash
# 运行网络诊断工具
./diagnose-network.sh
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

### 步骤2: 设置环境变量 + 网络检测
- **🌐 智能网络检测**: 自动检测网络质量，为后续构建做准备
- 生成安全密钥
- 创建 `.env` 配置文件
- 配置域名和数据库信息
- 如果 `.env` 已存在，则跳过创建
- **网络状况评估**: 根据检测结果提供优化建议

### 步骤3: 构建Docker镜像 (智能化)
- **步骤3a**: 拉取基础镜像 (PostgreSQL, Redis, Node.js, Nginx)
- **步骤3b**: 智能构建后端镜像
  - 根据网络状况自动选择最适合的Dockerfile
  - 自动配置国内镜像源 (阿里云、淘宝npm)
  - 包含重试机制和缓存清理
  - 提供详细的构建进度反馈
- **步骤3c**: 构建前端镜像 (Nginx + 静态文件)
- 显示构建结果摘要

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

### 🌐 网络相关问题

1. **网络连接诊断**
   ```bash
   # 运行网络诊断工具
   ./diagnose-network.sh
   ```

2. **网络状况较差时的解决方案**
   - 系统会自动使用轻量级Dockerfile (`backend/Dockerfile.lite`)
   - 建议在网络状况较好时重新构建
   - 考虑使用VPN或更换网络环境
   - 手动清理Docker缓存: `docker system prune -a`

3. **构建超时或失败**
   - 系统自动重试2次，每次间隔30秒
   - 自动清理失败的构建缓存
   - 查看详细错误信息并按提示操作

### 🐳 Docker相关问题

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

### 🔄 重新部署选项

1. **完全重新部署**
   ```bash
   # 清理所有容器和数据
   ./manage-services.sh clean
   
   # 重新执行部署
   ./deploy-all.sh
   ```

2. **仅重新构建应用**
   ```bash
   # 重新构建并启动 (保留数据)
   ./manage-services.sh rebuild
   ```

3. **分步骤重新构建**
   ```bash
   # 仅重新构建后端
   ./03b-build-backend.sh
   
   # 仅重新构建前端
   ./03c-build-nginx.sh
   ```

### 🚨 常见错误及解决方案

| 错误类型 | 可能原因 | 解决方案 |
|---------|---------|---------||
| 网络超时 | 网络连接不稳定 | 运行 `./diagnose-network.sh` 诊断 |
| 构建失败 | 依赖下载失败 | 系统自动重试，或手动重新运行 |
| 端口占用 | 其他服务占用端口 | 停止冲突服务或修改端口配置 |
| 权限错误 | 脚本无执行权限 | 运行 `chmod +x deployment/*.sh` |
| 磁盘空间不足 | Docker镜像占用过多空间 | 运行 `docker system prune -a` |
| 数据导入失败 | 数据库连接或文件权限问题 | 运行 `./07-data-import.sh` 或查看 `DATA_IMPORT_GUIDE.md` |

### 📊 数据导入故障排除

1. **数据库连接问题**
   ```bash
   # 检查数据库连接
   docker exec newland-postgres psql -U newland_user -d newland_db -c "SELECT 1;"
   ```

2. **文件上传权限问题**
   ```bash
   # 检查文件权限
   docker exec newland-backend ls -la /app/public/uploads/
   
   # 修复权限
   docker exec newland-backend chown -R node:node /app/public/uploads/
   ```

3. **导入工具使用**
   ```bash
   # 运行数据导入工具
   ./07-data-import.sh
   
   # 查看详细导入指南
   cat DATA_IMPORT_GUIDE.md
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