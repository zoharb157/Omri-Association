#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend
"""

import http.server
import os
import socketserver
import webbrowser

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Frontend server running on port {PORT}")
        print(f"📱 Access the dashboard at: http://localhost:{PORT}")
        print(f"🌍 Network access: http://10.100.102.7:{PORT}")
        print("🔗 No password protection - direct access!")
        print("✅ Connected to Python FastAPI backend")

        # Open browser automatically
        webbrowser.open(f'http://localhost:{PORT}')

        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
