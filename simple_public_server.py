#!/usr/bin/env python3
"""
Simple public server for Streamlit dashboard
"""

import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


class StreamlitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Forward request to Streamlit
            url = f"http://localhost:8501{self.path}"
            req = urllib.request.Request(url)

            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ["host", "connection"]:
                    req.add_header(header, value)

            # Make request
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)

                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ["content-encoding", "transfer-encoding"]:
                        self.send_header(header, value)
                self.end_headers()

                # Copy response body
                self.wfile.write(response.read())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            # Forward request to Streamlit
            url = f"http://localhost:8501{self.path}"
            req = urllib.request.Request(url, data=post_data)
            req.add_header("Content-Length", str(len(post_data)))

            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ["host", "connection", "content-length"]:
                    req.add_header(header, value)

            # Make request
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)

                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ["content-encoding", "transfer-encoding"]:
                        self.send_header(header, value)
                self.end_headers()

                # Copy response body
                self.wfile.write(response.read())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())


def start_server():
    PORT = 8080

    with HTTPServer(("0.0.0.0", PORT), StreamlitHandler) as httpd:
        print(f"🌐 Public server running on port {PORT}")
        print(f"📱 Access the dashboard at: http://localhost:{PORT}")
        print(f"🌍 Network access: http://10.100.102.7:{PORT}")
        print("🔗 No password protection - direct access!")
        print("✅ All your original views are preserved!")

        # Open browser automatically
        webbrowser.open(f"http://localhost:{PORT}")

        httpd.serve_forever()


if __name__ == "__main__":
    start_server()
