#!/bin/bash

# 🚀 NewLand 一键部署脚本
# 按顺序执行所有部署步骤

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 主函数
main() {
    show_banner
    echo "🚀 NewLand 一键部署"
    echo "═══════════════════════════════════════════════════════════════"
    echo "即将按顺序执行以下步骤:"
    echo "  1️⃣  检查Docker环境"
    echo "  2️⃣  设置环境变量"
    echo "  3️⃣  构建Docker镜像"
    echo "  4️⃣  启动服务"
    echo "  5️⃣  等待服务就绪并验证"
    echo
    
    read -p "是否继续？(y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log_info "部署已取消"
        exit 0
    fi
    
    echo
    log_info "开始执行部署流程..."
    echo
    
    # 获取脚本目录
    SCRIPT_DIR="$(dirname "$0")"
    
    # 步骤1: 检查Docker环境
    log_info "执行步骤1: 检查Docker环境"
    bash "$SCRIPT_DIR/01-check-docker.sh"
    echo
    
    # 步骤2: 设置环境变量
    log_info "执行步骤2: 设置环境变量"
    bash "$SCRIPT_DIR/02-setup-environment.sh"
    echo
    
    # 步骤3: 构建Docker镜像
    log_info "执行步骤3: 构建Docker镜像"
    bash "$SCRIPT_DIR/03-build-images.sh"
    echo
    
    # 步骤4: 启动服务
    log_info "执行步骤4: 启动服务"
    bash "$SCRIPT_DIR/04-start-services.sh"
    echo
    
    # 步骤5: 等待服务就绪并验证
    log_info "执行步骤5: 等待服务就绪并验证"
    bash "$SCRIPT_DIR/05-wait-and-verify.sh"
    
    echo
    log_success "🎉 一键部署完成！"
}

# 处理中断信号
trap 'echo -e "\n${RED}部署被中断${NC}"; exit 1' INT TERM

# 运行主函数
main "$@"