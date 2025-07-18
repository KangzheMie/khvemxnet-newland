#!/bin/bash

# 🚀 步骤4: 启动服务
# 停止现有服务并启动新的Docker容器

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 启动服务
start_services() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_docker "开始启动服务..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "deployment/docker-compose.yml" ]; then
        log_error "找不到 deployment/docker-compose.yml 文件"
        exit 1
    fi
    
    # 使用deployment目录下的docker-compose.yml
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 停止现有服务
    log_docker "停止现有服务..."
    docker compose -f "$COMPOSE_FILE" down --remove-orphans 2>/dev/null || true
    
    # 启动服务
    log_docker "启动服务..."
    docker compose -f "$COMPOSE_FILE" up -d
    
    log_success "服务启动完成"
    
    # 显示服务状态
    echo
    log_info "服务状态:"
    docker compose -f "$COMPOSE_FILE" ps
    echo
}

# 主函数
main() {
    show_banner
    echo "🚀 步骤4: 启动服务"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    start_services
    
    log_success "✅ 步骤4完成！服务已启动"
    echo "下一步: 运行 ./05-wait-and-verify.sh 等待服务就绪并验证"
}

# 运行主函数
main "$@"