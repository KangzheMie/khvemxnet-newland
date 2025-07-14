#!/bin/bash

# 🔍 步骤1: 检查Docker环境
# 验证Docker和Docker Compose是否正确安装和运行

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 检查Docker和Docker Compose
check_docker() {
    log_info "检查Docker环境..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        echo "安装指南: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose v2 未安装或未正确配置，请先安装或更新 Docker Desktop"
        echo "安装指南: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # 检查Docker是否运行
    if ! docker info &> /dev/null; then
        log_error "Docker服务未运行，请启动Docker服务"
        exit 1
    fi
    
    log_success "Docker环境检查通过"
    
    # 显示版本信息
    echo
    log_info "Docker版本信息:"
    docker --version
    docker compose version
    echo
}

# 主函数
main() {
    show_banner
    echo "🔍 步骤1: Docker环境检查"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    check_docker
    
    log_success "✅ 步骤1完成！Docker环境检查通过"
    echo "下一步: 运行 ./02-setup-environment.sh 设置环境变量"
}

# 运行主函数
main "$@"