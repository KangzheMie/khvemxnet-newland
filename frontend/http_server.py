#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级HTTP调试服务器
适用于Windows环境下的前端开发调试

使用方法:
    python debug_server.py [port] [directory]
    
参数:
    port: 端口号 (默认: 8080)
    directory: 服务目录 (默认: 当前目录)
    
示例:
    python debug_server.py 3000 ./frontend
    python debug_server.py 8080
    python debug_server.py
"""

import os
import sys
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote
import datetime
import mimetypes

class DebugHTTPRequestHandler(SimpleHTTPRequestHandler):
    """增强的HTTP请求处理器，支持CORS和详细日志"""
    
    def __init__(self, *args, **kwargs):
        # 添加常见的MIME类型
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('application/json', '.json')
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        """添加CORS头部"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        message = format % args
        
        # 根据状态码设置颜色（Windows CMD支持ANSI转义序列）
        if '200' in message:
            color = '\033[92m'  # 绿色
        elif '404' in message:
            color = '\033[91m'  # 红色
        elif '304' in message:
            color = '\033[93m'  # 黄色
        else:
            color = '\033[94m'  # 蓝色
        
        reset_color = '\033[0m'
        
        print(f"{color}[{timestamp}] {client_ip} - {message}{reset_color}")
    
    def guess_type(self, path):
        """改进的MIME类型猜测"""
        # 特殊处理一些文件类型
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.json'):
            return 'application/json'
        elif path.endswith('.svg'):
            return 'image/svg+xml'
        
        # 使用父类方法
        return super().guess_type(path)

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def is_port_available(port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8080, max_attempts=100):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None

def print_server_info(port, directory, local_ip):
    """打印服务器信息"""
    print("\n" + "="*60)
    print("🚀 轻量级HTTP调试服务器已启动")
    print("="*60)
    print(f"📁 服务目录: {os.path.abspath(directory)}")
    print(f"🌐 本地访问: http://localhost:{port}")
    print(f"🌐 网络访问: http://{local_ip}:{port}")
    print(f"⏰ 启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("💡 提示:")
    print("   - 按 Ctrl+C 停止服务器")
    print("   - 支持CORS跨域请求")
    print("   - 自动禁用缓存便于调试")
    print("   - 支持热重载（修改文件后刷新页面即可）")
    print("="*60)
    print("📊 访问日志:")
    print()

def main():
    """主函数"""
    # 启用Windows控制台ANSI颜色支持
    if sys.platform == "win32":
        os.system('color')
    
    # 解析命令行参数
    port = 8080
    directory = "."
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 错误: 端口号必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        directory = sys.argv[2]
        if not os.path.exists(directory):
            print(f"❌ 错误: 目录 '{directory}' 不存在")
            sys.exit(1)
    
    # 检查端口是否可用
    if not is_port_available(port):
        print(f"⚠️  警告: 端口 {port} 已被占用，正在寻找可用端口...")
        available_port = find_available_port(port)
        if available_port:
            port = available_port
            print(f"✅ 找到可用端口: {port}")
        else:
            print("❌ 错误: 无法找到可用端口")
            sys.exit(1)
    
    # 切换到服务目录
    original_dir = os.getcwd()
    os.chdir(directory)
    
    try:
        # 获取本机IP
        local_ip = get_local_ip()
        
        # 创建HTTP服务器
        server = HTTPServer(('', port), DebugHTTPRequestHandler)
        
        # 打印服务器信息
        print_server_info(port, directory, local_ip)
        
        # 启动服务器
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
        print("👋 感谢使用轻量级HTTP调试服务器！")
    except Exception as e:
        print(f"\n❌ 服务器错误: {e}")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)

if __name__ == "__main__":
    main()