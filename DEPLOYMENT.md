# Deployment Guide

## Table of Contents
- [Deployment Options](#deployment-options)
- [Frontend Deployment](#frontend-deployment)
- [Backend Deployment](#backend-deployment)
- [Environment Configuration](#environment-configuration)
- [SSL/HTTPS Setup](#sslhttps-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Scaling](#scaling)

---

## Deployment Options

### Recommended Platforms

**Frontend:**
- Vercel (Recommended)
- Netlify
- AWS S3 + CloudFront
- GitHub Pages

**Backend:**
- Railway
- Render
- AWS EC2
- Google Cloud Run
- DigitalOcean App Platform
- Heroku

---

## Frontend Deployment

### Option 1: Vercel (Easiest)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   npm run build
   vercel --prod
   ```

4. **Configure Environment Variables**:
   - Go to Vercel dashboard
   - Add `VITE_API_URL=https://your-backend-url.com`

### Option 2: Netlify

1. **Create `netlify.toml`**:
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. **Deploy via CLI**:
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify deploy --prod
   ```

3. **Or connect GitHub**:
   - Link repository in Netlify dashboard
   - Auto-deploy on push

### Option 3: AWS S3 + CloudFront

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Create S3 bucket**:
   ```bash
   aws s3 mb s3://your-bucket-name
   ```

3. **Upload build files**:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name
   ```

4. **Configure bucket for static hosting**

5. **Set up CloudFront distribution**

---

## Backend Deployment

### Option 1: Railway (Recommended)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**:
   ```bash
   railway login
   ```

3. **Initialize project**:
   ```bash
   cd backend
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Set environment variables** in Railway dashboard

### Option 2: Render

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: lung-ai-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.10.0
   ```

2. **Connect GitHub repository**

3. **Deploy from dashboard**

### Option 3: Docker + Any Cloud Provider

1. **Create Dockerfile**:
   ```dockerfile
   # backend/Dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application
   COPY . .

   # Expose port
   EXPOSE 8000

   # Run application
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build image**:
   ```bash
   docker build -t lung-ai-backend .
   ```

3. **Run container**:
   ```bash
   docker run -p 8000:8000 lung-ai-backend
   ```

4. **Deploy to cloud**:
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances

### Option 4: Traditional VPS (DigitalOcean, AWS EC2)

1. **SSH into server**:
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip nginx
   ```

3. **Clone repository**:
   ```bash
   git clone https://github.com/your-repo.git
   cd lung-disorder-detection/backend
   ```

4. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create systemd service** (`/etc/systemd/system/lungai.service`):
   ```ini
   [Unit]
   Description=Lung AI Backend
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/backend
   Environment="PATH=/path/to/backend/venv/bin"
   ExecStart=/path/to/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

6. **Enable and start service**:
   ```bash
   sudo systemctl enable lungai
   sudo systemctl start lungai
   ```

7. **Configure Nginx** (`/etc/nginx/sites-available/lungai`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/lungai /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

---

## Environment Configuration

### Frontend Environment Variables

Create `.env.production`:
```env
VITE_API_URL=https://api.your-domain.com
VITE_ENV=production
```

### Backend Environment Variables

Create `.env` or configure in cloud platform:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# CORS
CORS_ORIGINS=https://your-frontend-domain.com

# Model
MODEL_PATH=/app/models/hybrid_mobilenet_vit.h5

# Security
SECRET_KEY=your-secret-key-here

# Logging
LOG_LEVEL=INFO
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

1. **Install Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain certificate**:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal**:
   ```bash
   sudo certbot renew --dry-run
   ```

### Using CloudFlare (Easiest)

1. Add domain to CloudFlare
2. Update nameservers
3. Enable SSL (Flexible or Full)
4. Done! Automatic SSL

---

## Monitoring & Logging

### Application Monitoring

**Backend Logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

**Error Tracking** - Use Sentry:
```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### Performance Monitoring

**Tools:**
- New Relic
- Datadog
- Prometheus + Grafana
- AWS CloudWatch

**Example - Prometheus metrics**:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## Scaling

### Horizontal Scaling

**Load Balancer Configuration**:
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### Database Caching

If you add a database:
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### CDN for Static Assets

Use CDN for frontend assets:
- CloudFlare
- AWS CloudFront
- Fastly

### Auto-Scaling

**AWS Auto Scaling Group**:
- Set up EC2 instances
- Configure target tracking
- Set min/max instances

**Kubernetes**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: lungai-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: lungai-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Security Checklist

- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Add API authentication
- [ ] Sanitize user inputs
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable security headers
- [ ] Set up firewall rules
- [ ] Regular security audits
- [ ] Implement logging and monitoring
- [ ] Set up automated backups

---

## Post-Deployment

### 1. Verify Deployment
```bash
# Check frontend
curl https://your-domain.com

# Check backend
curl https://api.your-domain.com/api/health
```

### 2. Performance Testing
```bash
# Install Apache Bench
apt-get install apache2-utils

# Load test
ab -n 1000 -c 10 https://api.your-domain.com/api/health
```

### 3. Set Up Monitoring Alerts

Configure alerts for:
- High error rates
- Slow response times
- Server downtime
- High memory usage
- Disk space

### 4. Documentation

Update documentation with:
- Production URLs
- API endpoints
- Deployment procedures
- Rollback procedures

---

## Rollback Procedure

If deployment fails:

1. **Revert to previous version**:
   ```bash
   # Vercel
   vercel rollback

   # Git-based deployment
   git revert HEAD
   git push origin main
   ```

2. **Check logs**:
   ```bash
   # View backend logs
   tail -f /var/log/lungai/app.log
   ```

3. **Restore database** (if applicable)

4. **Notify users** of the issue and resolution

---

## Cost Optimization

### Free Tier Options

**Frontend**:
- Vercel: Free for personal projects
- Netlify: 100GB bandwidth/month free
- GitHub Pages: Free for public repos

**Backend**:
- Railway: $5 credit/month free
- Render: 750 hours/month free
- Fly.io: Free tier available

### Paid Recommendations

**Small Scale** ($10-50/month):
- Vercel Pro + Railway
- Netlify + Render

**Medium Scale** ($100-500/month):
- AWS (EC2 + S3 + CloudFront)
- Google Cloud Platform

**Large Scale** ($500+/month):
- Kubernetes on AWS/GCP
- Dedicated servers
- CDN + Load balancers

---

## Support

For deployment issues:
- Check deployment platform documentation
- Review application logs
- Test API endpoints
- Verify environment variables
- Check CORS configuration

---

**Good luck with your deployment! 🚀**
