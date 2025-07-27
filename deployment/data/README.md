# 数据导入目录结构

本目录用于存放待导入的数据文件。请按照以下结构组织您的数据：

## 目录结构

```
data/
├── sql/                    # 数据库 SQL 文件
│   ├── users.sql          # 用户数据
│   ├── articles.sql       # 文章数据
│   ├── categories.sql     # 分类数据
│   └── settings.sql       # 系统设置
├── uploads/               # 上传文件
│   ├── images/           # 图片文件
│   ├── documents/        # 文档文件
│   └── media/            # 其他媒体文件
└── README.md             # 本说明文件
```

## 使用说明

### SQL 文件

将您的数据库导出文件放入 `sql/` 目录：

```bash
# 示例：导出现有数据
pg_dump -U username -d database_name > data/sql/backup.sql

# 或者创建特定表的导出
pg_dump -U username -d database_name -t table_name > data/sql/table_name.sql
```

### 上传文件

将媒体文件放入 `uploads/` 目录：

```bash
# 复制图片文件
cp /path/to/images/* data/uploads/images/

# 复制文档文件
cp /path/to/documents/* data/uploads/documents/
```

## 导入流程

1. **准备数据**
   ```bash
   # 创建目录结构
   mkdir -p data/sql
   mkdir -p data/uploads/images
   mkdir -p data/uploads/documents
   mkdir -p data/uploads/media
   ```

2. **放置文件**
   - 将 SQL 文件放入 `data/sql/`
   - 将媒体文件放入 `data/uploads/` 的相应子目录

3. **执行导入**
   ```bash
   # 运行数据导入脚本
   ./07-data-import.sh
   ```

## 注意事项

- SQL 文件应使用 UTF-8 编码
- 确保 SQL 语法与 PostgreSQL 兼容
- 大文件建议分批导入
- 导入前建议备份现有数据

## 示例文件

### 示例 SQL 文件 (users.sql)

```sql
-- 插入用户数据
INSERT INTO users (username, email, password, created_at) VALUES 
('admin', 'admin@example.com', '$2b$10$...', NOW()),
('user1', 'user1@example.com', '$2b$10$...', NOW());
```

### 示例文件组织

```
data/uploads/
├── images/
│   ├── logo.png
│   ├── banner.jpg
│   └── avatar.jpg
├── documents/
│   ├── manual.pdf
│   └── guide.docx
└── media/
    ├── video.mp4
    └── audio.mp3
```

导入后，这些文件将被复制到 Strapi 的上传目录，并可通过以下 URL 访问：
- `http://localhost:1337/uploads/logo.png`
- `http://localhost:1337/uploads/banner.jpg`
- 等等...

## 相关文档

- [数据导入详细指南](../DATA_IMPORT_GUIDE.md)
- [部署文档](../README.md)