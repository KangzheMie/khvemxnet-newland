#!/bin/bash

# 🔍 网络诊断脚本
# 检查Docker构建相关的网络连接问题

set -e

# 导入通用函数
source "$(dirname "$0")/common.sh"

# 诊断网络连接
diagnose_network() {
    show_banner
    echo "🔍 网络连接诊断"
    echo "═══════════════════════════════════════════════════════════════"
    echo
    
    log_info "检查基础网络连接..."
    
    # 检查DNS解析
    echo "📡 DNS解析测试:"
    if nslookup dl-cdn.alpinelinux.org > /dev/null 2>&1; then
        echo "  ✅ Alpine官方源DNS解析正常"
    else
        echo "  ❌ Alpine官方源DNS解析失败"
    fi
    
    if nslookup mirrors.aliyun.com > /dev/null 2>&1; then
        echo "  ✅ 阿里云镜像源DNS解析正常"
    else
        echo "  ❌ 阿里云镜像源DNS解析失败"
    fi
    
    if nslookup registry.npmmirror.com > /dev/null 2>&1; then
        echo "  ✅ npm淘宝镜像源DNS解析正常"
    else
        echo "  ❌ npm淘宝镜像源DNS解析失败"
    fi
    
    echo
    
    # 检查网络连通性
    echo "🌐 网络连通性测试:"
    if curl -s --connect-timeout 10 https://mirrors.aliyun.com > /dev/null; then
        echo "  ✅ 阿里云镜像源连接正常"
    else
        echo "  ❌ 阿里云镜像源连接失败"
    fi
    
    if curl -s --connect-timeout 10 https://registry.npmmirror.com > /dev/null; then
        echo "  ✅ npm淘宝镜像源连接正常"
    else
        echo "  ❌ npm淘宝镜像源连接失败"
    fi
    
    if curl -s --connect-timeout 10 https://hub.docker.com > /dev/null; then
        echo "  ✅ Docker Hub连接正常"
    else
        echo "  ❌ Docker Hub连接失败"
    fi
    
    echo
    
    # 检查Docker状态
    echo "🐳 Docker状态检查:"
    if docker info > /dev/null 2>&1; then
        echo "  ✅ Docker服务运行正常"
        echo "  📊 Docker信息:"
        docker info | grep -E "(Server Version|Storage Driver|Logging Driver|Cgroup Driver)" | sed 's/^/    /'
    else
        echo "  ❌ Docker服务异常"
    fi
    
    echo
    
    # 检查磁盘空间
    echo "💾 磁盘空间检查:"
    df -h / | tail -1 | awk '{
        if ($5+0 > 90) 
            print "  ❌ 磁盘空间不足: " $5 " 已使用"
        else if ($5+0 > 80)
            print "  ⚠️  磁盘空间紧张: " $5 " 已使用"
        else
            print "  ✅ 磁盘空间充足: " $5 " 已使用"
    }'
    
    echo
    
    # 检查内存使用
    echo "🧠 内存使用检查:"
    free -h | awk 'NR==2{
        if ($3/$2*100 > 90)
            print "  ❌ 内存使用过高: " $3 "/" $2
        else if ($3/$2*100 > 80)
            print "  ⚠️  内存使用较高: " $3 "/" $2
        else
            print "  ✅ 内存使用正常: " $3 "/" $2
    }'
    
    echo
    
    # 提供建议
    echo "💡 优化建议:"
    echo "  1. 如果网络连接有问题，建议："
    echo "     - 检查防火墙设置"
    echo "     - 尝试使用VPN"
    echo "     - 更换网络环境"
    echo
    echo "  2. 如果Docker有问题，建议："
    echo "     - 重启Docker服务: sudo systemctl restart docker"
    echo "     - 清理Docker缓存: docker system prune -a"
    echo "     - 检查Docker配置文件"
    echo
    echo "  3. 如果资源不足，建议："
    echo "     - 清理不必要的文件和容器"
    echo "     - 增加虚拟内存"
    echo "     - 关闭其他占用资源的程序"
    
    log_success "网络诊断完成"
}

# 主函数
main() {
    diagnose_network
}

# 运行主函数
main "$@"