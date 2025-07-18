#!/bin/bash

# 🚀 NewLand 一键部署脚本
# 自动执行完整的部署流程

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 主函数
main() {
    show_banner
    echo "🚀 NewLand 一键部署"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    log_info "开始执行完整部署流程..."
    echo
    
    # 步骤1: 检查Docker环境
    log_info "🔍 执行步骤1: 检查Docker环境"
    ./01-check-docker.sh
    echo
    
    # 步骤2: 设置环境变量
    log_info "⚙️ 执行步骤2: 设置环境变量"
    ./02-setup-environment.sh
    echo
    
    # 步骤3: 构建Docker镜像
    log_info "🏗️ 执行步骤3: 构建Docker镜像"
    ./03-build-images.sh
    echo
    
    # 步骤4: 启动服务
    log_info "🚀 执行步骤4: 启动服务"
    ./04-start-services.sh
    echo
    
    # 步骤5: 等待服务就绪并验证
    log_info "⏳ 执行步骤5: 等待服务就绪并验证"
    ./05-wait-and-verify.sh
    echo
    
    log_success "🎉 NewLand 部署完成！"
    echo
    echo "═══════════════════════════════════════════════════════════════"
    echo "🌐 访问地址:"
    echo "   前端: http://localhost"
    echo "   后端API: http://localhost/api"
    echo "   管理后台: http://localhost/admin"
    echo
    echo "🛠️ 管理命令:"
    echo "   查看状态: ./manage-services.sh status"
    echo "   查看日志: ./manage-services.sh logs"
    echo "   重启服务: ./manage-services.sh restart"
    echo "   停止服务: ./manage-services.sh stop"
    echo "═══════════════════════════════════════════════════════════════"
}

# 运行主函数
main "$@"