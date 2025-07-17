#!/bin/bash

# 🏗️ 智能构建脚本
# 根据网络状况选择最适合的构建方式

set -e

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 检测网络状况
check_network_quality() {
    log_info "检测网络状况..."
    
    local score=0
    local total_tests=4
    
    # 测试1: DNS解析速度
    if timeout 5 nslookup mirrors.aliyun.com > /dev/null 2>&1; then
        score=$((score + 1))
    fi
    
    # 测试2: 阿里云镜像连接
    if timeout 10 curl -s https://mirrors.aliyun.com > /dev/null 2>&1; then
        score=$((score + 1))
    fi
    
    # 测试3: npm镜像连接
    if timeout 10 curl -s https://registry.npmmirror.com > /dev/null 2>&1; then
        score=$((score + 1))
    fi
    
    # 测试4: Docker Hub连接
    if timeout 10 curl -s https://hub.docker.com > /dev/null 2>&1; then
        score=$((score + 1))
    fi
    
    local quality=$((score * 100 / total_tests))
    
    if [ $quality -ge 75 ]; then
        echo "good"
    elif [ $quality -ge 50 ]; then
        echo "fair"
    else
        echo "poor"
    fi
}

# 智能构建函数
smart_build() {
    cd_to_project_root
    
    log_info "开始智能构建..."
    
    # 检测网络质量
    local network_quality=$(check_network_quality)
    
    case $network_quality in
        "good")
            log_success "网络状况良好，使用完整版Dockerfile"
            dockerfile="backend/Dockerfile"
            ;;
        "fair")
            log_info "网络状况一般，使用优化版Dockerfile"
            dockerfile="backend/Dockerfile"
            ;;
        "poor")
            log_info "网络状况较差，使用轻量级Dockerfile"
            dockerfile="backend/Dockerfile.lite"
            ;;
    esac
    
    log_info "使用Dockerfile: $dockerfile"
    
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
                echo "  5. 重启Docker服务: sudo systemctl restart docker"
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
    echo "🏗️ 智能后端构建"
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
    
    smart_build
    
    log_success "✅ 智能构建完成！"
    echo "下一步: 运行 ./03c-build-nginx.sh 构建前端镜像"
}

# 运行主函数
main "$@"