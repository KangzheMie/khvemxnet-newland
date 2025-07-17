#!/bin/bash

# 🏗️ 步骤3b: 构建后端镜像
# 智能构建Strapi后端应用镜像，根据网络状况选择最适合的构建方式

set -e

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 智能构建函数
build_backend() {
    cd_to_project_root
    
    log_info "开始智能构建后端镜像..."
    
    # 使用通用网络检测功能
    local network_quality=$(check_network_quality)
    local dockerfile=$(get_dockerfile_choice)
    
    log_info "使用Dockerfile: $dockerfile"
    show_network_optimization
    
    # 修改docker-compose.yml临时使用指定的Dockerfile
    local compose_file="deployment/docker-compose.yml"
    local backup_file="deployment/docker-compose.yml.backup"
    
    # 备份原文件
    cp "$compose_file" "$backup_file"
    
    # 修改dockerfile路径
    sed -i "s|dockerfile: backend/Dockerfile|dockerfile: $dockerfile|g" "$compose_file"
    
    # 构建镜像
    log_docker "开始构建后端镜像..."
    
    # 设置构建参数
    local timeout_duration=1800  # 30分钟
    local max_retries=2
    local retry_count=0
    
    # 清理构建缓存
    docker builder prune -f || true
    
    while [ $retry_count -lt $max_retries ]; do
        log_info "构建尝试 $((retry_count + 1))/$max_retries"
        
        if timeout $timeout_duration docker compose -f "$compose_file" build --no-cache backend; then
            log_success "后端镜像构建成功！"
            break
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                log_info "构建失败，等待30秒后重试..."
                sleep 30
                docker builder prune -f || true
            else
                log_error "构建失败，已达到最大重试次数"
                
                # 恢复原文件
                mv "$backup_file" "$compose_file"
                
                echo
                log_info "故障排除建议："
                echo "  1. 运行网络诊断: ./diagnose-network.sh"
                echo "  2. 检查防火墙和代理设置"
                echo "  3. 尝试更换网络环境"
                echo "  4. 手动清理Docker: docker system prune -a"
                echo "  5. 重启Docker服务"
                exit 1
            fi
        fi
    done
    
    # 恢复原文件
    mv "$backup_file" "$compose_file"
    
    # 显示构建结果
    echo
    log_info "构建的后端镜像:"
    docker images | grep -E "(newland.*backend|deployment.*backend)" || echo "未找到后端镜像"
    echo
}

# 主函数
main() {
    show_banner
    echo "🏗️ 步骤3b: 智能构建后端镜像"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    # 检查必要文件
    if [ ! -f "backend/package.json" ]; then
        log_error "找不到 backend/package.json 文件"
        exit 1
    fi
    
    if [ ! -f "backend/Dockerfile" ]; then
        log_error "找不到 backend/Dockerfile 文件"
        exit 1
    fi
    
    # 验证package.json
    log_info "验证package.json语法..."
    if ! node -e "JSON.parse(require('fs').readFileSync('backend/package.json', 'utf8'))" 2>/dev/null; then
        log_error "backend/package.json 语法错误"
        exit 1
    fi
    log_success "package.json 语法验证通过"
    
    build_backend
    
    log_success "✅ 步骤3b完成！后端镜像构建完成"
    echo "下一步: 运行 ./03c-build-nginx.sh 构建前端镜像"
}

# 运行主函数
main "$@"