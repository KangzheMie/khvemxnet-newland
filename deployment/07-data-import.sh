#!/bin/bash

# 数据导入脚本
# 用于导入数据库内容和文件内容到 NewLand 项目

set -e

echo "=== NewLand 数据导入工具 ==="
echo "此脚本帮助您导入数据库内容和文件内容"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Docker 服务状态
check_services() {
    echo -e "${BLUE}检查服务状态...${NC}"
    
    if ! docker compose ps | grep -q "Up"; then
        echo -e "${RED}错误: 服务未运行，请先启动服务${NC}"
        echo "运行: ./04-start-services.sh"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 服务正在运行${NC}"
}

# 数据库内容导入
import_database() {
    echo
    echo -e "${BLUE}=== 数据库内容导入 ===${NC}"
    echo
    
    # 检查是否有 SQL 导入文件
    if [ -d "./data/sql" ]; then
        echo "发现 SQL 文件目录: ./data/sql"
        echo "可用的 SQL 文件:"
        ls -la ./data/sql/*.sql 2>/dev/null || echo "未找到 .sql 文件"
        echo
        
        read -p "请输入要导入的 SQL 文件路径 (或按 Enter 跳过): " sql_file
        
        if [ -n "$sql_file" ] && [ -f "$sql_file" ]; then
            echo -e "${YELLOW}导入 SQL 文件: $sql_file${NC}"
            
            # 复制 SQL 文件到容器并执行
            docker cp "$sql_file" deployment-postgres:/tmp/import.sql
            docker exec deployment-postgres psql -U newland_user -d newland_db -f /tmp/import.sql
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ SQL 文件导入成功${NC}"
            else
                echo -e "${RED}✗ SQL 文件导入失败${NC}"
            fi
        else
            echo "跳过 SQL 文件导入"
        fi
    else
        echo -e "${YELLOW}未找到 ./data/sql 目录${NC}"
        echo "如需导入 SQL 文件，请:"
        echo "1. 创建 ./data/sql 目录"
        echo "2. 将 .sql 文件放入该目录"
        echo "3. 重新运行此脚本"
    fi
    
    echo
    echo "手动数据库导入方法:"
    echo "1. 连接到数据库容器:"
    echo "   docker exec -it deployment-postgres psql -U newland_user -d newland_db"
    echo "2. 或者从外部连接:"
    echo "   psql -h localhost -p 5432 -U newland_user -d newland_db"
    echo "3. 执行 SQL 命令或导入文件"
}

# 文件内容导入
import_files() {
    echo
    echo -e "${BLUE}=== 文件内容导入 ===${NC}"
    echo
    
    echo "后端文件组织结构:"
    echo "- 上传文件存储在: backend/public/uploads/"
    echo "- Strapi 会自动生成多种尺寸的图片:"
    echo "  * 原始文件: filename.ext"
    echo "  * 缩略图: thumbnail_filename.ext"
    echo "  * 小图: small_filename.ext"
    echo "  * 中图: medium_filename.ext"
    echo "  * 大图: large_filename.ext"
    echo
    
    # 检查是否有文件导入目录
    if [ -d "./data/uploads" ]; then
        echo "发现文件导入目录: ./data/uploads"
        echo "目录内容:"
        ls -la ./data/uploads/ 2>/dev/null || echo "目录为空"
        echo
        
        read -p "是否要将 ./data/uploads/ 中的文件复制到后端? (y/N): " copy_files
        
        if [[ $copy_files =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}复制文件到后端容器...${NC}"
            
            # 确保目标目录存在
            docker exec deployment-backend mkdir -p /app/public/uploads
            
            # 复制文件
            docker cp ./data/uploads/. deployment-backend:/app/public/uploads/
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ 文件复制成功${NC}"
                
                # 设置正确的权限
                docker exec deployment-backend chown -R node:node /app/public/uploads
                docker exec deployment-backend chmod -R 755 /app/public/uploads
                
                echo -e "${GREEN}✓ 文件权限设置完成${NC}"
            else
                echo -e "${RED}✗ 文件复制失败${NC}"
            fi
        else
            echo "跳过文件复制"
        fi
    else
        echo -e "${YELLOW}未找到 ./data/uploads 目录${NC}"
        echo "如需导入文件，请:"
        echo "1. 创建 ./data/uploads 目录"
        echo "2. 将要导入的文件放入该目录"
        echo "3. 重新运行此脚本"
    fi
    
    echo
    echo "手动文件导入方法:"
    echo "1. 直接复制到容器:"
    echo "   docker cp /path/to/your/files deployment-backend:/app/public/uploads/"
    echo "2. 或者复制到本地后端目录:"
    echo "   cp /path/to/your/files ../backend/public/uploads/"
    echo "3. 设置正确权限:"
    echo "   docker exec deployment-backend chown -R node:node /app/public/uploads"
    echo "   docker exec deployment-backend chmod -R 755 /app/public/uploads"
}

# 验证导入结果
verify_import() {
    echo
    echo -e "${BLUE}=== 验证导入结果 ===${NC}"
    echo
    
    # 检查数据库连接
    echo "检查数据库连接..."
    if docker exec deployment-postgres psql -U newland_user -d newland_db -c "SELECT 1;" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ 数据库连接正常${NC}"
        
        # 显示表信息
        echo "数据库表信息:"
        docker exec deployment-postgres psql -U newland_user -d newland_db -c "\dt" 2>/dev/null || echo "无法获取表信息"
    else
        echo -e "${RED}✗ 数据库连接失败${NC}"
    fi
    
    echo
    
    # 检查上传文件
    echo "检查上传文件..."
    file_count=$(docker exec deployment-backend find /app/public/uploads -type f 2>/dev/null | wc -l)
    echo "上传目录文件数量: $file_count"
    
    if [ "$file_count" -gt 0 ]; then
        echo -e "${GREEN}✓ 发现上传文件${NC}"
        echo "最近的文件:"
        docker exec deployment-backend ls -la /app/public/uploads/ | head -10
    else
        echo -e "${YELLOW}! 未发现上传文件${NC}"
    fi
}

# 显示访问信息
show_access_info() {
    echo
    echo -e "${BLUE}=== 访问信息 ===${NC}"
    echo
    echo "前端访问地址: http://localhost:3000"
    echo "后端 API: http://localhost:1337"
    echo "管理面板: http://localhost:1337/admin"
    echo "数据库: localhost:5432"
    echo
    echo "如果导入了新数据，建议:"
    echo "1. 重启后端服务以刷新缓存"
    echo "2. 检查管理面板中的内容"
    echo "3. 测试前端页面显示"
}

# 主函数
main() {
    check_services
    
    echo "请选择导入类型:"
    echo "1. 数据库内容导入"
    echo "2. 文件内容导入"
    echo "3. 完整导入 (数据库 + 文件)"
    echo "4. 仅验证当前状态"
    echo
    
    read -p "请输入选择 (1-4): " choice
    
    case $choice in
        1)
            import_database
            verify_import
            ;;
        2)
            import_files
            verify_import
            ;;
        3)
            import_database
            import_files
            verify_import
            ;;
        4)
            verify_import
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            exit 1
            ;;
    esac
    
    show_access_info
    
    echo
    echo -e "${GREEN}数据导入流程完成！${NC}"
}

# 执行主函数
main "$@"