#!/bin/bash

# 🛠️ NewLand 部署工具函数库
# 提供通用的日志和工具函数

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_docker() {
    echo -e "${PURPLE}[DOCKER]${NC} $1"
}

# 显示横幅
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🐳 NewLand Docker部署                    ║"
    echo "║                     模块化部署脚本 v2.0                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 生成随机密钥
generate_secret() {
    if command -v openssl &> /dev/null; then
        openssl rand -base64 32 | tr -d "\n"
    else
        # 备用方法
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1
    fi
}

# 定义项目根目录变量
PROJECT_ROOT=""

# 设置并切换到项目根目录
# 这个函数应该在每个主脚本的开头被调用一次
setup_project_root() {
    if [ -z "$PROJECT_ROOT" ]; then
        # 使用readlink -f来获取脚本的绝对路径，然后找到根目录
        local script_path=$(readlink -f "${BASH_SOURCE[0]}")
        local deployment_dir=$(dirname "$script_path")
        PROJECT_ROOT=$(dirname "$deployment_dir")
        log_info "项目根目录已设置为: $PROJECT_ROOT"
    fi
    cd "$PROJECT_ROOT"
    log_info "当前工作目录: $(pwd)"
}

# 兼容旧的函数名，但现在它只做cd操作
cd_to_project_root() {
    if [ -z "$PROJECT_ROOT" ]; then
        echo "Error: PROJECT_ROOT is not set. Please call setup_project_root() first."
        exit 1
    fi
    cd "$PROJECT_ROOT"
    # log_info "Switched to project root: $(pwd)" # 减少重复日志
}

# 全局网络质量变量
NETWORK_QUALITY=""
DOCKERFILE_CHOICE=""

# 检测网络质量
check_network_quality() {
    if [ -n "$NETWORK_QUALITY" ]; then
        # 如果已经检测过，直接返回结果
        echo "$NETWORK_QUALITY"
        return
    fi
    
    log_info "🌐 检测网络状况..."
    
    local score=0
    local total_tests=4
    
    # 测试1: DNS解析速度
    if timeout 5 nslookup mirrors.aliyun.com > /dev/null 2>&1; then
        score=$((score + 1))
        echo "  ✅ 阿里云镜像源DNS解析正常"
    else
        echo "  ❌ 阿里云镜像源DNS解析失败"
    fi
    
    # 测试2: 阿里云镜像连接
    if timeout 10 curl -s https://mirrors.aliyun.com > /dev/null 2>&1; then
        score=$((score + 1))
        echo "  ✅ 阿里云镜像源连接正常"
    else
        echo "  ❌ 阿里云镜像源连接失败"
    fi
    
    # 测试3: npm镜像连接
    if timeout 10 curl -s https://registry.npmmirror.com > /dev/null 2>&1; then
        score=$((score + 1))
        echo "  ✅ npm淘宝镜像源连接正常"
    else
        echo "  ❌ npm淘宝镜像源连接失败"
    fi
    
    # 测试4: Docker Hub连接
    if timeout 10 curl -s https://hub.docker.com > /dev/null 2>&1; then
        score=$((score + 1))
        echo "  ✅ Docker Hub连接正常"
    else
        echo "  ❌ Docker Hub连接失败"
    fi
    
    local quality_percentage=$((score * 100 / total_tests))
    
    if [ $quality_percentage -ge 75 ]; then
        NETWORK_QUALITY="good"
        DOCKERFILE_CHOICE="backend/Dockerfile"
        log_success "网络状况良好 ($quality_percentage%)，将使用完整版Dockerfile"
    elif [ $quality_percentage -ge 50 ]; then
        NETWORK_QUALITY="fair"
        DOCKERFILE_CHOICE="backend/Dockerfile"
        log_warning "网络状况一般 ($quality_percentage%)，将使用优化版Dockerfile"
    else
        NETWORK_QUALITY="poor"
        DOCKERFILE_CHOICE="backend/Dockerfile.lite"
        log_warning "网络状况较差 ($quality_percentage%)，将使用轻量级Dockerfile"
    fi
    
    echo "$NETWORK_QUALITY"
}

# 获取推荐的Dockerfile路径
get_dockerfile_choice() {
    if [ -z "$DOCKERFILE_CHOICE" ]; then
        check_network_quality > /dev/null
    fi
    echo "$DOCKERFILE_CHOICE"
}

# 显示网络优化建议
show_network_optimization() {
    case "$NETWORK_QUALITY" in
        "poor")
            echo
            log_info "🔧 网络优化建议："
            echo "  1. 检查网络连接是否稳定"
            echo "  2. 尝试使用VPN或更换网络环境"
            echo "  3. 考虑使用国内镜像源"
            echo "  4. 如果问题持续，可运行 ./diagnose-network.sh 进行详细诊断"
            ;;
        "fair")
            echo
            log_info "💡 网络提示："
            echo "  网络状况一般，构建过程可能需要更长时间"
            echo "  如遇到问题，可尝试重新运行或使用 ./diagnose-network.sh 诊断"
            ;;
        "good")
            echo
            log_success "🚀 网络状况良好，预期构建过程顺利"
            ;;
    esac
}