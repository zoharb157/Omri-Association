#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import threading
import time
import webbrowser

def start_streamlit():
    """Start Streamlit in the background"""
    subprocess.run([
        'python3', '-m', 'streamlit', 'run', 'dashboard.py',
        '--server.port', '8501',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true'
    ])

def start_http_server():
    """Start a simple HTTP server that proxies to Streamlit"""
    PORT = 8080
    
    class ProxyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                import urllib.request
                url = f"http://localhost:8501{self.path}"
                req = urllib.request.Request(url)
                
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        if header.lower() not in ['content-encoding', 'transfer-encoding']:
                            self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
        
        def do_HEAD(self):
            self.do_GET()
        
        def do_POST(self):
            try:
                import urllib.request
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                url = f"http://localhost:8501{self.path}"
                req = urllib.request.Request(url, data=post_data)
                req.add_header('Content-Length', str(len(post_data)))
                
                for header, value in self.headers.items():
                    if header.lower() not in ['host', 'connection', 'content-length']:
                        req.add_header(header, value)
                
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        if header.lower() not in ['content-encoding', 'transfer-encoding']:
                            self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
    
    with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
        print(f"🌐 Server running on port {PORT}")
        print(f"📱 Local access: http://localhost:{PORT}")
        print(f"🌍 Network access: http://10.100.102.7:{PORT}")
        print("🔗 No password protection - direct access!")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start Streamlit in background
    print("🚀 Starting Streamlit...")
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Wait for Streamlit to start
    time.sleep(5)
    
    # Start HTTP server
    start_http_server()
