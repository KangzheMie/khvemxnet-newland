#!/bin/bash

# 🏗️ 步骤3: 构建Docker镜像
# 统一构建所有Docker镜像的主脚本

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3: 构建Docker镜像"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    # 显示网络状况（如果之前已检测过）
    if [ -n "$NETWORK_QUALITY" ]; then
        log_info "当前网络状况: $NETWORK_QUALITY"
        echo "将使用Dockerfile: $(get_dockerfile_choice)"
        echo
    fi
    
    log_info "开始构建所有Docker镜像..."
    echo
    
    # 步骤3a: 拉取基础镜像
    log_info "🔄 执行步骤3a: 拉取基础镜像"
    ./03a-pull-base-images.sh
    echo
    
    # 步骤3b: 构建后端镜像
    log_info "🔄 执行步骤3b: 构建后端镜像"
    ./03b-build-backend.sh
    echo
    
    # 步骤3c: 构建前端镜像
    log_info "🔄 执行步骤3c: 构建前端镜像"
    ./03c-build-nginx.sh
    echo
    
    log_success "✅ 步骤3完成！所有Docker镜像构建完成"
    echo
    
    # 显示构建结果摘要
    log_info "📋 构建结果摘要:"
    echo "───────────────────────────────────────────────────────────────"
    docker images | grep -E "(newland|postgres|redis|nginx)" | head -10 || echo "未找到相关镜像"
    echo
    
    echo "下一步: 运行 ./04-start-services.sh 启动服务"
}

# 运行主函数
main "$@"