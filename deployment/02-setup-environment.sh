#!/bin/bash

# ⚙️ 步骤2: 设置环境变量
# 创建或检查.env文件，生成必要的密钥和配置

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置环境变量
setup_environment() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_info "设置环境变量..."
    
    if [ ! -f .env ]; then
        log_info "创建环境配置文件..."
        
        # 生成随机密钥
        log_info "生成安全密钥..."
        DB_PASSWORD=$(generate_secret)
        APP_KEYS=$(generate_secret)
        API_TOKEN_SALT=$(generate_secret)
        ADMIN_JWT_SECRET=$(generate_secret)
        TRANSFER_TOKEN_SALT=$(generate_secret)
        JWT_SECRET=$(generate_secret)
        
        # 询问域名
        read -p "请输入域名 (默认: localhost): " DOMAIN
        DOMAIN=${DOMAIN:-localhost}
        
        # 创建.env文件
        cat > .env << EOF
# NewLand Docker部署环境变量
# 自动生成于 $(date)

# 安全配置
DB_PASSWORD=$DB_PASSWORD
APP_KEYS=$APP_KEYS
API_TOKEN_SALT=$API_TOKEN_SALT
ADMIN_JWT_SECRET=$ADMIN_JWT_SECRET
TRANSFER_TOKEN_SALT=$TRANSFER_TOKEN_SALT
JWT_SECRET=$JWT_SECRET

# 域名配置
DOMAIN=$DOMAIN

# 数据库配置
DATABASE_NAME=newland_db
DATABASE_USERNAME=newland_user

# 环境配置
NODE_ENV=production
TZ=Asia/Shanghai
EOF
        
        log_success "环境配置文件已创建"
        echo "📁 文件位置: $(pwd)/.env"
    else
        log_info "使用现有的环境配置文件"
        echo "📁 文件位置: $(pwd)/.env"
    fi
    
    # 显示配置摘要
    echo
    log_info "当前配置摘要:"
    echo "   域名: $(grep DOMAIN .env | cut -d'=' -f2)"
    echo "   数据库: $(grep DATABASE_NAME .env | cut -d'=' -f2)"
    echo "   环境: $(grep NODE_ENV .env | cut -d'=' -f2)"
    echo
}

# 主函数
main() {
    show_banner
    echo "⚙️ 步骤2: 环境变量设置"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    # 进行网络检测，为后续构建做准备
    echo "🌐 网络环境检测"
    echo "───────────────────────────────────────────────────────────────"
    check_network_quality > /dev/null
    show_network_optimization
    echo
    
    setup_environment
    
    log_success "✅ 步骤2完成！环境变量已设置"
    echo "下一步: 运行 ./03-build-images.sh 构建Docker镜像"
    
    # 根据网络状况给出建议
    if [ "$NETWORK_QUALITY" = "poor" ]; then
        echo
        log_warning "⚠️  由于网络状况较差，建议："
        echo "  • 在构建前运行 ./diagnose-network.sh 进行详细网络诊断"
        echo "  • 考虑在网络状况较好时进行构建"
        echo "  • 构建过程将自动使用轻量级配置以提高成功率"
    fi
}

# 运行主函数
main "$@"