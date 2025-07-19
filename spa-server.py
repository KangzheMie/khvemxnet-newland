#!/usr/bin/env python3
"""
🌐 NewLand2 SPA开发服务器
支持单页应用路由的简单HTTP服务器
"""

import http.server
import socketserver
import os
import mimetypes
from urllib.parse import urlparse

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    """支持SPA路由的HTTP请求处理器"""
    
    def do_GET(self):
        # 解析请求路径
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 如果是根路径，直接返回index.html
        if path == '/':
            self.path = '/index.html'
            return super().do_GET()
        
        # 检查文件是否存在
        file_path = self.translate_path(path)
        
        # 如果是静态资源文件（有扩展名），直接处理
        if '.' in os.path.basename(path):
            return super().do_GET()
        
        # 如果文件不存在且不是静态资源，返回index.html（SPA路由）
        if not os.path.exists(file_path):
            self.path = '/index.html'
            return super().do_GET()
        
        # 其他情况正常处理
        return super().do_GET()
    
    def end_headers(self):
        # 添加CORS头部（开发环境）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"🌐 {self.address_string()} - {format % args}")

def run_server(port=8000):
    """启动SPA服务器"""
    handler = SPAHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 NewLand2 SPA服务器启动成功！")
        print(f"📍 访问地址: http://localhost:{port}")
        print(f"🔧 支持SPA路由重写")
        print(f"⏹️  按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)