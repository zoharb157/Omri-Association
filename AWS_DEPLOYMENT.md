# AWS Deployment Guide for Omri Association Dashboard

This guide will help you deploy the Omri Association Dashboard on AWS using Docker.

## Prerequisites

- AWS Account
- EC2 instance (recommended: t3.medium or larger)
- Docker and Docker Compose installed on your EC2 instance
- Google Sheets service account JSON file

## Step 1: Launch EC2 Instance

1. **Launch EC2 Instance:**
   - Choose Ubuntu 22.04 LTS
   - Instance type: t3.medium (2 vCPU, 4GB RAM) or larger
   - Storage: 20GB minimum
   - Security Group: Allow inbound traffic on port 8501

2. **Security Group Configuration:**
   ```
   Type: Custom TCP
   Port: 8501
   Source: 0.0.0.0/0 (or your specific IP range)
   ```

## Step 2: Install Docker on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply group changes
exit
```

## Step 3: Deploy the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zoharb157/Omri-Association.git
   cd Omri-Association
   ```

2. **Place your service account file:**
   ```bash
   # Copy your Google Sheets service account JSON file
   cp /path/to/your/service_account.json ./service_account.json
   ```

3. **Create logs directory:**
   ```bash
   mkdir -p logs
   ```

4. **Deploy with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## Step 4: Verify Deployment

1. **Check if container is running:**
   ```bash
   docker-compose ps
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f omri-dashboard
   ```

3. **Access the dashboard:**
   - Open browser and go to: `http://your-ec2-public-ip:8501`

## Step 5: Set Up Domain (Optional)

1. **Get a domain name** (e.g., from Route 53 or any domain provider)

2. **Point domain to your EC2 instance:**
   - Create an A record pointing to your EC2 public IP

3. **Set up SSL with Let's Encrypt:**
   ```bash
   # Install nginx
   sudo apt install nginx -y
   
   # Install certbot
   sudo apt install certbot python3-certbot-nginx -y
   
   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com
   ```

## Step 6: Configure Nginx Reverse Proxy (Optional)

Create nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/omri-dashboard
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/omri-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Step 7: Set Up Auto-Start

Create a systemd service for auto-start:

```bash
sudo nano /etc/systemd/system/omri-dashboard.service
```

Add this content:

```ini
[Unit]
Description=Omri Association Dashboard
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/Omri-Association
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable omri-dashboard.service
sudo systemctl start omri-dashboard.service
```

## Step 8: Monitoring and Maintenance

1. **View application logs:**
   ```bash
   docker-compose logs -f
   ```

2. **Update the application:**
   ```bash
   git pull
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. **Backup data:**
   ```bash
   # Backup logs
   tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
   
   # Backup service account (if needed)
   cp service_account.json service_account-backup.json
   ```

## Environment Variables

You can customize the deployment by setting these environment variables in `docker-compose.yml`:

- `SERVICE_ACCOUNT_FILE`: Path to Google Sheets service account JSON
- `SPREADSHEET_ID`: Main spreadsheet ID
- `WIDOW_SPREADSHEET_ID`: Widow data spreadsheet ID
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Troubleshooting

1. **Container won't start:**
   ```bash
   docker-compose logs omri-dashboard
   ```

2. **Port already in use:**
   ```bash
   sudo netstat -tulpn | grep :8501
   sudo kill -9 <PID>
   ```

3. **Permission issues:**
   ```bash
   sudo chown -R ubuntu:ubuntu /home/ubuntu/Omri-Association
   ```

## Security Considerations

1. **Use a reverse proxy** (nginx) with SSL
2. **Restrict access** by IP if possible
3. **Keep the service account file secure**
4. **Regular updates** of the application and system
5. **Monitor logs** for any suspicious activity

## Cost Optimization

- Use **Spot Instances** for development
- **Stop/Start** instances when not in use
- Use **t3.small** for light usage
- Consider **AWS Fargate** for serverless container deployment
