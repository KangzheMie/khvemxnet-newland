#!/bin/bash

# 🛠️ NewLand2 服务管理脚本
# 提供停止、重启、清理等管理功能

set -e  # 遇到错误立即退出

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 显示帮助信息
show_help() {
    echo "用法: $0 [命令]"
    echo
    echo "可用命令:"
    echo "  status    - 显示服务状态"
    echo "  logs      - 显示服务日志"
    echo "  stop      - 停止所有服务"
    echo "  restart   - 重启所有服务"
    echo "  clean     - 清理所有容器和卷"
    echo "  rebuild   - 重新构建并启动服务"
    echo "  help      - 显示此帮助信息"
    echo
}

# 显示服务状态
show_status() {
    cd_to_project_root
    
    log_info "服务状态:"
    docker compose -f "deployment/docker-compose.yml" ps
    echo
    
    log_info "资源使用情况:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# 显示服务日志
show_logs() {
    cd_to_project_root
    
    echo "选择要查看日志的服务:"
    echo "  1) 所有服务"
    echo "  2) 后端 (backend)"
    echo "  3) 前端 (nginx)"
    echo "  4) 数据库 (postgres)"
    echo "  5) 缓存 (redis)"
    echo
    
    read -p "请选择 (1-5): " choice
    
    case $choice in
        1)
            log_info "显示所有服务日志 (按Ctrl+C退出):"
            docker compose -f "deployment/docker-compose.yml" logs -f
            ;;
        2)
            log_info "显示后端服务日志 (按Ctrl+C退出):"
            docker compose -f "deployment/docker-compose.yml" logs -f backend
            ;;
        3)
            log_info "显示前端服务日志 (按Ctrl+C退出):"
            docker compose -f "deployment/docker-compose.yml" logs -f nginx
            ;;
        4)
            log_info "显示数据库服务日志 (按Ctrl+C退出):"
            docker compose -f "deployment/docker-compose.yml" logs -f postgres
            ;;
        5)
            log_info "显示缓存服务日志 (按Ctrl+C退出):"
            docker compose -f "deployment/docker-compose.yml" logs -f redis
            ;;
        *)
            log_error "无效选择"
            exit 1
            ;;
    esac
}

# 停止服务
stop_services() {
    cd_to_project_root
    
    log_info "停止所有服务..."
    docker compose -f "deployment/docker-compose.yml" down
    log_success "服务已停止"
}

# 重启服务
restart_services() {
    cd_to_project_root
    
    log_info "重启所有服务..."
    docker compose -f "deployment/docker-compose.yml" restart
    log_success "服务已重启"
    
    echo
    show_status
}

# 清理服务
clean_services() {
    cd_to_project_root
    
    echo -e "${RED}⚠️  警告: 此操作将删除所有容器、网络和数据卷！${NC}"
    echo "这将清除所有数据，包括数据库内容和上传的文件。"
    echo
    read -p "确定要继续吗？(输入 'YES' 确认): " confirm
    
    if [ "$confirm" != "YES" ]; then
        log_info "清理操作已取消"
        exit 0
    fi
    
    log_warning "开始清理..."
    docker compose -f "deployment/docker-compose.yml" down -v --remove-orphans
    
    # 清理相关镜像
    log_info "清理相关镜像..."
    docker images | grep newland2 | awk '{print $3}' | xargs -r docker rmi || true
    
    log_success "清理完成"
}

# 重新构建服务
rebuild_services() {
    cd_to_project_root
    
    log_info "重新构建并启动服务..."
    
    # 停止现有服务
    docker compose -f "deployment/docker-compose.yml" down
    
    # 重新构建
    docker compose -f "deployment/docker-compose.yml" build --no-cache
    
    # 启动服务
    docker compose -f "deployment/docker-compose.yml" up -d
    
    log_success "重新构建完成"
    
    echo
    show_status
}

# 主函数
main() {
    show_banner
    echo "🛠️ NewLand2 服务管理"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    case "${1:-help}" in
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        clean)
            clean_services
            ;;
        rebuild)
            rebuild_services
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"