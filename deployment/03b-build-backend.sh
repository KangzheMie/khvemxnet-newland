#!/bin/bash

# 🏗️ 步骤3b: 构建后端镜像
# 单独构建Strapi后端应用镜像

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 构建后端镜像
build_backend() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_docker "开始构建后端镜像..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "deployment/docker-compose.yml" ]; then
        log_error "找不到 deployment/docker-compose.yml 文件"
        exit 1
    fi
    
    # 检查backend目录和关键文件
    if [ ! -f "backend/package.json" ]; then
        log_error "找不到 backend/package.json 文件"
        exit 1
    fi
    
    if [ ! -f "backend/Dockerfile" ]; then
        log_error "找不到 backend/Dockerfile 文件"
        exit 1
    fi
    
    # 验证package.json语法
    log_info "验证package.json语法..."
    if ! node -e "JSON.parse(require('fs').readFileSync('backend/package.json', 'utf8'))" 2>/dev/null; then
        log_error "backend/package.json 语法错误，请检查JSON格式"
        exit 1
    fi
    log_success "package.json 语法验证通过"
    
    # 使用deployment目录下的docker-compose.yml
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 构建后端镜像
    log_docker "构建Strapi后端镜像..."
    docker compose -f "$COMPOSE_FILE" build --no-cache backend
    
    log_success "后端镜像构建完成"
    
    # 显示构建的镜像
    echo
    log_info "构建的后端镜像:"
    docker images | grep -E "(newland.*backend|deployment.*backend)" || echo "未找到后端镜像"
    echo
}

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3b: 构建后端镜像"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    build_backend
    
    log_success "✅ 步骤3b完成！后端镜像构建完成"
    echo "下一步: 运行 ./03c-build-nginx.sh 构建前端镜像"
}

# 运行主函数
main "$@"