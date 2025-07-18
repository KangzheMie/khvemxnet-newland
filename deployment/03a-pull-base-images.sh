#!/bin/bash

# 🏗️ 步骤3a: 拉取基础镜像
# 拉取PostgreSQL和Redis基础镜像

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 拉取基础镜像
pull_base_images() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_docker "开始拉取基础镜像..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "deployment/docker-compose.yml" ]; then
        log_error "找不到 deployment/docker-compose.yml 文件"
        exit 1
    fi
    
    # 使用deployment目录下的docker-compose.yml
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 拉取基础镜像
    log_docker "拉取PostgreSQL镜像..."
    docker compose -f "$COMPOSE_FILE" pull postgres || {
        log_warning "PostgreSQL镜像拉取失败，将在构建时自动下载"
    }
    
    log_docker "拉取Redis镜像..."
    docker compose -f "$COMPOSE_FILE" pull redis || {
        log_warning "Redis镜像拉取失败，将在构建时自动下载"
    }
    
    log_docker "拉取Node.js基础镜像..."
    docker pull node:20-alpine || {
        log_warning "Node.js镜像拉取失败，将在构建时自动下载"
    }
    
    log_docker "拉取Nginx基础镜像..."
    docker pull nginx:alpine || {
        log_warning "Nginx镜像拉取失败，将在构建时自动下载"
    }
    
    log_success "基础镜像拉取完成"
    
    # 显示拉取的镜像
    echo
    log_info "已拉取的基础镜像列表:"
    docker images | grep -E "(postgres|redis|node|nginx)" || echo "未找到相关镜像"
    echo
}

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3a: 拉取基础镜像"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    pull_base_images
    
    log_success "✅ 步骤3a完成！基础镜像拉取完成"
    echo "下一步: 运行 ./03b-build-backend.sh 构建后端镜像"
}

# 运行主函数
main "$@"