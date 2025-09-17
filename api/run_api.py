#!/usr/bin/env python3
"""
Startup script for Omri Association API
"""

import os
import sys

import uvicorn

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("🚀 Starting Omri Association API...")
    print("📊 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔗 Health check at: http://localhost:8000/api/health")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
