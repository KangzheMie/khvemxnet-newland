#!/bin/bash

# 🏗️ 步骤3: 构建Docker镜像
# 拉取基础镜像并构建自定义应用镜像

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 构建镜像
build_images() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_docker "开始构建Docker镜像..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "deployment/docker-compose.yml" ]; then
        log_error "找不到 deployment/docker-compose.yml 文件"
        exit 1
    fi
    
    # 使用deployment目录下的docker-compose.yml
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 拉取基础镜像
    log_docker "拉取基础镜像..."
    docker compose -f "$COMPOSE_FILE" pull postgres redis || {
        log_warning "部分基础镜像拉取失败，将在构建时自动下载"
    }
    
    # 构建自定义镜像
    log_docker "构建应用镜像..."
    docker compose -f "$COMPOSE_FILE" build --no-cache
    
    log_success "镜像构建完成"
    
    # 显示构建的镜像
    echo
    log_info "构建的镜像列表:"
    docker images | grep -E "(newland|postgres|redis|nginx)" || echo "未找到相关镜像"
    echo
}

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3: Docker镜像构建"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    build_images
    
    log_success "✅ 步骤3完成！Docker镜像构建完成"
    echo "下一步: 运行 ./04-start-services.sh 启动服务"
}

# 运行主函数
main "$@"