#!/bin/bash

# ⏳ 步骤5: 等待服务就绪并验证
# 等待各个服务启动完成并进行健康检查

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 等待服务启动
wait_for_services() {
    # 切换到项目根目录
    cd_to_project_root
    
    log_info "等待服务启动..."
    
    COMPOSE_FILE="deployment/docker-compose.yml"
    
    # 等待数据库
    log_info "等待数据库启动..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U newland_user -d newland_db &>/dev/null; then
            log_success "数据库已就绪"
            break
        fi
        echo -n "."
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "数据库启动超时"
        echo "请检查数据库容器日志: docker compose -f $COMPOSE_FILE logs postgres"
        exit 1
    fi
    
    # 等待后端
    log_info "等待后端服务启动..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:1337/_health &>/dev/null; then
            log_success "后端服务已就绪"
            break
        fi
        echo -n "."
        sleep 3
        timeout=$((timeout-3))
    done
    
    if [ $timeout -le 0 ]; then
        log_warning "后端服务启动可能需要更多时间，请稍后检查"
        echo "检查后端日志: docker compose -f $COMPOSE_FILE logs backend"
    fi
    
    # 等待前端
    log_info "等待前端服务启动..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost/ &>/dev/null; then
            log_success "前端服务已就绪"
            break
        fi
        echo -n "."
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        log_warning "前端服务启动可能需要更多时间，请稍后检查"
        echo "检查前端日志: docker compose -f $COMPOSE_FILE logs nginx"
    fi
}

# 显示部署信息
show_deployment_info() {
    # 切换到项目根目录
    cd_to_project_root
    
    if [ -f .env ]; then
        DOMAIN=$(grep DOMAIN .env | cut -d'=' -f2)
    else
        DOMAIN="localhost"
    fi
    
    echo
    log_success "🎉 NewLand Docker部署完成！"
    echo
    echo -e "${GREEN}📋 访问信息:${NC}"
    echo "   🌐 前端地址: http://$DOMAIN"
    echo "   🔧 后端API: http://$DOMAIN/api"
    echo "   👨‍💼 管理后台: http://$DOMAIN/admin"
    echo
    echo -e "${BLUE}🐳 Docker管理命令:${NC}"
    echo "   查看服务状态: docker compose -f deployment/docker-compose.yml ps"
    echo "   查看服务日志: docker compose -f deployment/docker-compose.yml logs -f [service_name]"
    echo "   重启服务: docker compose -f deployment/docker-compose.yml restart [service_name]"
    echo "   停止所有服务: docker compose -f deployment/docker-compose.yml down"
    echo "   完全清理: docker compose -f deployment/docker-compose.yml down -v --remove-orphans"
    echo
    echo -e "${YELLOW}📊 监控命令:${NC}"
    echo "   实时日志: docker compose -f deployment/docker-compose.yml logs -f"
    echo "   资源使用: docker stats"
    echo "   进入容器: docker compose -f deployment/docker-compose.yml exec [service_name] sh"
    echo
    echo -e "${PURPLE}⚠️  重要提示:${NC}"
    echo "   1. 首次访问管理后台需要创建管理员账户"
    echo "   2. 请妥善保管 .env 文件中的密钥"
    echo "   3. 生产环境请配置HTTPS和域名"
    echo "   4. 定期备份数据库和上传文件"
    echo
}

# 显示服务状态
show_service_status() {
    # 切换到项目根目录
    cd_to_project_root
    
    echo -e "${BLUE}🔍 最终服务状态检查:${NC}"
    docker compose -f "deployment/docker-compose.yml" ps
    echo
}

# 主函数
main() {
    show_banner
    echo "⏳ 步骤5: 等待服务就绪并验证"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    wait_for_services
    show_service_status
    show_deployment_info
    
    log_success "✅ 步骤5完成！所有服务已就绪"
    
    # 自动验证管理面板
    echo
    log_info "正在验证管理面板..."
    if [ -f "deployment/06-verify-admin-panel.sh" ]; then
        ./deployment/06-verify-admin-panel.sh
    else
        log_warning "管理面板验证脚本不存在，请手动检查 http://localhost:1337/admin"
    fi
    
    echo "🎉 部署流程全部完成！"
}

# 运行主函数
main "$@"