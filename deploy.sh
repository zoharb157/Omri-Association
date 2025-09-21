#!/bin/bash

# Omri Association Dashboard Deployment Script
# This script helps deploy the dashboard on AWS EC2

set -e

echo "🚀 Starting Omri Association Dashboard Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if service account file exists
if [ ! -f "service_account.json" ]; then
    print_warning "service_account.json not found!"
    print_warning "Please place your Google Sheets service account JSON file in the project root."
    print_warning "You can get this file from Google Cloud Console."
    exit 1
fi

# Create logs directory
print_status "Creating logs directory..."
mkdir -p logs

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start containers
print_status "Building Docker image..."
docker-compose build --no-cache

print_status "Starting containers..."
docker-compose up -d

# Wait for container to be ready
print_status "Waiting for application to start..."
sleep 10

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    print_status "✅ Dashboard is running successfully!"
    print_status "🌐 Access your dashboard at: http://localhost:8501"
    print_status "📊 Or use your EC2 public IP: http://$(curl -s ifconfig.me):8501"
    
    # Show container status
    echo ""
    print_status "Container Status:"
    docker-compose ps
    
    # Show logs
    echo ""
    print_status "Recent logs:"
    docker-compose logs --tail=20
    
else
    print_error "❌ Failed to start dashboard. Check logs:"
    docker-compose logs
    exit 1
fi

echo ""
print_status "🎉 Deployment completed successfully!"
print_status "📝 For more information, see AWS_DEPLOYMENT.md"
