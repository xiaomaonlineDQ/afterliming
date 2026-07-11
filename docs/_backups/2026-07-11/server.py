"""黎明之后 - 本地开发服务器（禁用浏览器缓存）"""
import http.server
import socketserver
import os

PORT = 8081
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

print(f"\n黎明之后开发服务器")
print(f"地址: http://localhost:{PORT}")
print(f"缓存: 已禁用 (每次刷新都加载最新文件)")
print(f"按 Ctrl+C 停止\n")

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
