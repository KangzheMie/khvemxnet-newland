#!/bin/bash

# 🏗️ 步骤3c: 构建前端镜像
# 单独构建Nginx前端应用镜像

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 构建前端镜像
build_nginx() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_docker "开始构建前端镜像..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "deployment/docker-compose.yml" ]; then
        log_error "找不到 deployment/docker-compose.yml 文件"
        exit 1
    fi
    
    # 检查前端目录和关键文件
    if [ ! -d "frontend" ]; then
        log_error "找不到 frontend 目录"
        exit 1
    fi
    
    if [ ! -f "index.html" ]; then
        log_error "找不到 index.html 文件"
        exit 1
    fi
    
    if [ ! -f "deployment/Dockerfile.nginx" ]; then
        log_error "找不到 deployment/Dockerfile.nginx 文件"
        exit 1
    fi
    
    if [ ! -f "deployment/nginx.conf" ]; then
        log_error "找不到 deployment/nginx.conf 文件"
        exit 1
    fi
    
    # 使用deployment目录下的docker-compose.yml
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 构建前端镜像
    log_docker "构建Nginx前端镜像..."
    docker compose -f "$COMPOSE_FILE" build --no-cache nginx
    
    log_success "前端镜像构建完成"
    
    # 显示构建的镜像
    echo
    log_info "构建的前端镜像:"
    docker images | grep -E "(newland.*nginx|deployment.*nginx)" || echo "未找到前端镜像"
    echo
}

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3c: 构建前端镜像"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    build_nginx
    
    log_success "✅ 步骤3c完成！前端镜像构建完成"
    echo "下一步: 运行 ./04-start-services.sh 启动服务"
}

# 运行主函数
main "$@"