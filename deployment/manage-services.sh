#!/bin/bash

# 🛠️ NewLand 服务管理脚本
# 用于管理 NewLand Docker 服务的启动、停止、重启等操作

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 显示帮助信息
show_help() {
    echo "🛠️ NewLand 服务管理脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  stop      停止所有服务"
    echo "  restart   重启所有服务"
    echo "  clean     清理未使用的Docker资源"
    echo "  rebuild   重建并重启所有服务"
    echo "  status    查看服务状态"
    echo "  logs      查看服务日志"
    echo "  help      显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 stop     # 停止所有服务"
    echo "  $0 restart # 重启所有服务"
    echo "  $0 status  # 查看服务状态"
}

# 停止服务
stop_services() {
    echo "🛑 停止 NewLand 服务..."
    
    cd_to_project_root
    
    COMPOSE_FILE="deployment/docker-compose.yml"

    if [ -f "$COMPOSE_FILE" ]; then
        docker compose -f "$COMPOSE_FILE" down
        echo "✅ 服务已停止"
    else
        log_error "找不到 docker-compose.yml 文件，路径: $(pwd)/$COMPOSE_FILE"
        exit 1
    fi
}

# 重启服务
restart_services() {
    echo "🔄 重启 NewLand 服务..."
    
    stop_services
    sleep 2
    
    echo "🚀 启动服务..."
    # 04-start-services.sh 内部会自己切换目录
    ./04-start-services.sh
    
    if [ $? -eq 0 ]; then
        echo "✅ 服务重启完成"
        ./05-wait-and-verify.sh
    else
        echo "❌ 服务重启失败"
        exit 1
    fi
}

# 清理Docker资源
clean_docker() {
    echo "🧹 清理未使用的Docker资源..."
    
    # 停止服务
    stop_services
    
    # 清理未使用的容器
    echo "清理停止的容器..."
    docker container prune -f
    
    # 清理未使用的镜像
    echo "清理悬空镜像..."
    docker image prune -f
    
    # 清理未使用的卷
    echo "清理未使用的卷..."
    docker volume prune -f
    
    # 清理未使用的网络
    echo "清理未使用的网络..."
    docker network prune -f
    
    echo "✅ Docker资源清理完成"
}

# 重建服务
rebuild_services() {
    echo "🔨 重建 NewLand 服务..."
    
    # 停止并清理
    stop_services
    
    # 清理项目相关的镜像
    echo "清理项目镜像..."
    docker images | grep newland | awk '{print $3}' | xargs -r docker rmi || true
    
    # 重新构建
    echo "重新构建镜像..."
    # 03-build-images.sh 内部会自己切换目录
    ./03-build-images.sh
    
    if [ $? -eq 0 ]; then
        echo "🚀 启动重建的服务..."
        ./04-start-services.sh
        
        if [ $? -eq 0 ]; then
            echo "✅ 服务重建完成"
            ./05-wait-and-verify.sh
        else
            echo "❌ 服务启动失败"
            exit 1
        fi
    else
        echo "❌ 镜像构建失败"
        exit 1
    fi
}

# 查看服务状态
show_status() {
    echo "📊 NewLand 服务状态"
    echo "==================="
    
    cd_to_project_root

    COMPOSE_FILE="deployment/docker-compose.yml"
    
    if [ -f "$COMPOSE_FILE" ]; then
        docker compose -f "$COMPOSE_FILE" ps
        echo ""
        echo "📈 资源使用情况:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    else
        log_error "找不到 docker-compose.yml 文件，路径: $(pwd)/$COMPOSE_FILE"
        exit 1
    fi
}

# 查看服务日志
show_logs() {
    echo "📋 NewLand 服务日志"
    echo "=================="
    
    cd_to_project_root

    COMPOSE_FILE="deployment/docker-compose.yml"
    
    if [ -f "$COMPOSE_FILE" ]; then
        echo "选择要查看的服务日志:"
        echo "1) 所有服务"
        echo "2) 数据库 (postgres)"
        echo "3) 后端 (backend)"
        echo "4) 前端 (nginx)"
        echo "5) 缓存 (redis)"
        
        read -p "请选择 (1-5): " choice
        
        case $choice in
            1)
                docker compose -f "$COMPOSE_FILE" logs -f
                ;;
            2)
                docker compose -f "$COMPOSE_FILE" logs -f postgres
                ;;
            3)
                docker compose -f "$COMPOSE_FILE" logs -f backend
                ;;
            4)
                docker compose -f "$COMPOSE_FILE" logs -f nginx
                ;;
            5)
                docker compose -f "$COMPOSE_FILE" logs -f redis
                ;;
            *)
                echo "❌ 无效选择"
                exit 1
                ;;
        esac
    else
        log_error "找不到 docker-compose.yml 文件，路径: $(pwd)/$COMPOSE_FILE"
        exit 1
    fi
}

# 主函数
main() {
    case "$1" in
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        clean)
            clean_docker
            ;;
        rebuild)
            rebuild_services
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            echo "🛠️ NewLand 服务管理"
            echo "请使用 '$0 help' 查看可用选项"
            ;;
        *)
            echo "❌ 未知选项: $1"
            echo "请使用 '$0 help' 查看可用选项"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"