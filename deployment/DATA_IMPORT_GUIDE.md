# 数据导入指南

本指南详细说明如何将现有数据导入到 NewLand 项目中，包括数据库内容和文件内容的导入方法。

## 概述

数据导入分为两个主要部分：
1. **数据库内容导入** - 导入结构化数据（文章、用户、配置等）
2. **文件内容导入** - 导入媒体文件（图片、附件等）

## 快速开始

### 自动化导入（推荐）

```bash
# 运行数据导入脚本
./07-data-import.sh
```

### 手动导入

参考下面的详细步骤进行手动导入。

## 数据库内容导入

### 准备工作

1. **确保服务运行**
   ```bash
   ./04-start-services.sh
   ./05-wait-and-verify.sh
   ```

2. **准备 SQL 文件**
   ```bash
   mkdir -p ./data/sql
   # 将您的 .sql 文件放入 ./data/sql/ 目录
   ```

### 导入方法

#### 方法一：使用脚本导入

```bash
./07-data-import.sh
# 选择选项 1 或 3
```

#### 方法二：手动导入

```bash
# 复制 SQL 文件到容器
docker cp your-data.sql deployment-postgres:/tmp/import.sql

# 执行 SQL 文件
docker exec deployment-postgres psql -U newland_user -d newland_db -f /tmp/import.sql
```

#### 方法三：交互式导入

```bash
# 连接到数据库
docker exec -it deployment-postgres psql -U newland_user -d newland_db

# 在 psql 中执行命令
\i /tmp/your-file.sql
# 或直接输入 SQL 命令
```

### 常见 SQL 导入示例

```sql
-- 导入用户数据
INSERT INTO users (username, email, password) VALUES 
('admin', 'admin@example.com', 'hashed_password');

-- 导入文章数据
INSERT INTO articles (title, content, author_id, created_at) VALUES 
('示例文章', '文章内容...', 1, NOW());

-- 导入分类数据
INSERT INTO categories (name, description) VALUES 
('技术', '技术相关文章');
```

## 文件内容导入

### Strapi 文件组织结构

Strapi 将上传的文件存储在 `backend/public/uploads/` 目录中，并自动生成多种尺寸：

```
backend/public/uploads/
├── original_file.jpg          # 原始文件
├── thumbnail_original_file.jpg # 缩略图 (150x150)
├── small_original_file.jpg     # 小图 (500x500)
├── medium_original_file.jpg    # 中图 (750x750)
└── large_original_file.jpg     # 大图 (1000x1000)
```

### 文件命名规则

Strapi 使用以下命名规则：
- 原始文件：`filename_hash.ext`
- 缩略图：`thumbnail_filename_hash.ext`
- 小图：`small_filename_hash.ext`
- 中图：`medium_filename_hash.ext`
- 大图：`large_filename_hash.ext`

其中 `hash` 是 Strapi 生成的唯一标识符。

### 导入方法

#### 方法一：使用脚本导入

```bash
# 准备文件
mkdir -p ./data/uploads
# 将您的文件放入 ./data/uploads/ 目录

# 运行导入脚本
./07-data-import.sh
# 选择选项 2 或 3
```

#### 方法二：直接复制到容器

```bash
# 复制文件到容器
docker cp ./your-files/ deployment-backend:/app/public/uploads/

# 设置正确权限
docker exec deployment-backend chown -R node:node /app/public/uploads
docker exec deployment-backend chmod -R 755 /app/public/uploads
```

#### 方法三：复制到本地目录

```bash
# 如果容器使用卷挂载
cp -r ./your-files/* ../backend/public/uploads/
```

### 文件权限注意事项

确保文件具有正确的权限：
- 所有者：`node:node`
- 权限：`755` (目录) / `644` (文件)

```bash
# 修复权限
docker exec deployment-backend chown -R node:node /app/public/uploads
docker exec deployment-backend find /app/public/uploads -type d -exec chmod 755 {} \;
docker exec deployment-backend find /app/public/uploads -type f -exec chmod 644 {} \;
```

## 完整导入流程

### 1. 准备阶段

```bash
# 创建数据目录
mkdir -p ./data/sql
mkdir -p ./data/uploads

# 准备您的数据文件
# - 将 .sql 文件放入 ./data/sql/
# - 将媒体文件放入 ./data/uploads/
```

### 2. 执行导入

```bash
# 确保服务运行
./04-start-services.sh
./05-wait-and-verify.sh

# 执行完整导入
./07-data-import.sh
# 选择选项 3 (完整导入)
```

### 3. 验证导入

```bash
# 检查数据库
docker exec deployment-postgres psql -U newland_user -d newland_db -c "\dt"

# 检查文件
docker exec deployment-backend ls -la /app/public/uploads/

# 访问管理面板验证
# http://localhost:1337/admin
```

## 故障排除

### 数据库导入问题

**问题：SQL 导入失败**
```bash
# 检查 SQL 语法
docker exec deployment-postgres psql -U newland_user -d newland_db -c "\q"

# 查看错误日志
docker logs deployment-postgres
```

**问题：权限不足**
```bash
# 确认数据库用户权限
docker exec deployment-postgres psql -U newland_user -d newland_db -c "\du"
```

**问题：编码问题**
```bash
# 设置正确的编码
docker exec deployment-postgres psql -U newland_user -d newland_db -c "SET client_encoding = 'UTF8';"
```

### 文件导入问题

**问题：文件无法访问**
```bash
# 检查文件权限
docker exec deployment-backend ls -la /app/public/uploads/

# 修复权限
docker exec deployment-backend chown -R node:node /app/public/uploads
docker exec deployment-backend chmod -R 755 /app/public/uploads
```

**问题：文件路径错误**
```bash
# 确认容器内路径
docker exec deployment-backend pwd
docker exec deployment-backend ls -la /app/public/
```

**问题：磁盘空间不足**
```bash
# 检查容器磁盘使用
docker exec deployment-backend df -h

# 检查主机磁盘使用
df -h
```

### 服务相关问题

**问题：服务未运行**
```bash
# 检查服务状态
docker compose ps

# 重启服务
./04-start-services.sh
```

**问题：数据库连接失败**
```bash
# 检查数据库日志
docker logs deployment-postgres

# 检查网络连接
docker exec deployment-backend ping deployment-postgres
```

## 最佳实践

### 导入前准备

1. **备份现有数据**
   ```bash
   # 备份数据库
   docker exec deployment-postgres pg_dump -U newland_user newland_db > backup.sql
   
   # 备份文件
   docker cp deployment-backend:/app/public/uploads ./backup-uploads
   ```

2. **验证数据格式**
   - 确保 SQL 文件语法正确
   - 检查文件格式和大小
   - 验证字符编码（推荐 UTF-8）

3. **测试小批量导入**
   - 先导入少量数据进行测试
   - 验证导入结果
   - 确认无误后进行完整导入

### 导入后验证

1. **数据完整性检查**
   ```bash
   # 检查记录数量
   docker exec deployment-postgres psql -U newland_user -d newland_db -c "SELECT COUNT(*) FROM your_table;"
   
   # 检查数据样本
   docker exec deployment-postgres psql -U newland_user -d newland_db -c "SELECT * FROM your_table LIMIT 5;"
   ```

2. **文件可访问性检查**
   ```bash
   # 通过 HTTP 访问文件
   curl -I http://localhost:1337/uploads/your-file.jpg
   
   # 检查文件权限
   docker exec deployment-backend ls -la /app/public/uploads/your-file.jpg
   ```

3. **功能测试**
   - 访问管理面板检查数据
   - 测试前端页面显示
   - 验证文件上传功能

### 性能优化

1. **大文件处理**
   - 分批导入大量文件
   - 使用压缩格式传输
   - 考虑使用外部存储服务

2. **数据库优化**
   - 导入前禁用索引
   - 使用事务批量插入
   - 导入后重建索引

3. **监控资源使用**
   - 监控磁盘空间
   - 检查内存使用
   - 观察 CPU 负载

## 相关文件

- `07-data-import.sh` - 自动化导入脚本
- `docker-compose.yml` - 服务配置
- `04-start-services.sh` - 服务启动脚本
- `05-wait-and-verify.sh` - 服务验证脚本

## 支持

如果遇到问题，请：
1. 查看相关日志文件
2. 检查服务状态
3. 参考故障排除部分
4. 联系技术支持