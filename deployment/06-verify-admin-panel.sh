#!/bin/bash

# 🔍 步骤6: 验证和修复管理面板
# 检查Strapi管理面板是否正确构建，如果没有则自动修复

set -e

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 设置项目根目录
setup_project_root

# 验证管理面板函数
verify_admin_panel() {
    log_info "检查管理面板状态..."
    
    # 检查容器是否运行
    if ! docker compose ps backend | grep -q "Up"; then
        log_error "Backend 容器未运行，请先启动服务"
        echo "运行: docker compose up -d backend"
        exit 1
    fi
    
    # 检查管理面板响应
    log_info "测试管理面板访问..."
    local admin_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:1337/admin || echo "000")
    
    if [ "$admin_response" = "200" ]; then
        log_success "✅ 管理面板正常访问"
        echo "管理面板地址: http://localhost:1337/admin"
        return 0
    elif [ "$admin_response" = "404" ]; then
        log_warning "⚠️  管理面板返回404，需要重新构建"
        return 1
    else
        log_warning "⚠️  管理面板响应异常 (HTTP $admin_response)"
        return 1
    fi
}

# 修复管理面板函数
fix_admin_panel() {
    log_info "开始修复管理面板..."
    
    # 进入容器构建管理面板
    log_info "在容器内构建管理面板..."
    if docker compose exec backend npm run build; then
        log_success "✅ 管理面板构建完成"
    else
        log_error "❌ 管理面板构建失败"
        return 1
    fi
    
    # 重启backend服务
    log_info "重启backend服务..."
    docker compose restart backend
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 10
    
    # 再次验证
    if verify_admin_panel; then
        log_success "✅ 管理面板修复成功！"
        return 0
    else
        log_error "❌ 管理面板修复失败"
        return 1
    fi
}

# 显示管理面板信息
show_admin_info() {
    echo
    log_info "管理面板信息:"
    echo "  📍 访问地址: http://localhost:1337/admin"
    echo "  🔑 首次访问需要创建管理员账户"
    echo "  📊 API地址: http://localhost:1337/api"
    echo
    
    # 显示API端点状态
    log_info "API端点测试:"
    local api_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:1337/api || echo "000")
    if [ "$api_response" = "404" ]; then
        echo "  ✅ API端点正常 (返回404是正常的，表示需要具体路径)"
    else
        echo "  ⚠️  API端点响应: HTTP $api_response"
    fi
}

# 主函数
main() {
    show_banner
    echo "🔍 步骤6: 验证和修复管理面板"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    # 切换到项目根目录
    cd_to_project_root
    
    # 验证管理面板
    if verify_admin_panel; then
        show_admin_info
        log_success "✅ 步骤6完成！管理面板工作正常"
    else
        log_info "管理面板需要修复，开始自动修复..."
        if fix_admin_panel; then
            show_admin_info
            log_success "✅ 步骤6完成！管理面板已修复"
        else
            log_error "❌ 管理面板修复失败"
            echo
            log_info "手动修复步骤:"
            echo "  1. 进入容器: docker compose exec backend sh"
            echo "  2. 构建管理面板: npm run build"
            echo "  3. 退出容器: exit"
            echo "  4. 重启服务: docker compose restart backend"
            echo "  5. 等待启动: sleep 10"
            echo "  6. 测试访问: curl http://localhost:1337/admin"
            exit 1
        fi
    fi
    
    echo "下一步: 在浏览器中访问 http://localhost:1337/admin"
}

# 运行主函数
main "$@"