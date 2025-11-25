# Fix 413 Request Entity Too Large Error

## Problem
Getting "413 Request Entity Too Large" error when uploading large files (>100MB) through Nginx.

## Solution
Updated both Flask and Nginx configurations to support 500MB file uploads.

## Deployment Steps on Cloud Server

### Step 1: Push Code Changes
```bash
# On local machine (already done)
git add config.py nginx_config.conf
git commit -m "Increased upload limit to 500MB"
git push origin master
```

### Step 2: SSH to Cloud Server
```bash
ssh prismappolice@control-room-dsr
# Or: ssh root@103.127.29.139
```

### Step 3: Update Code
```bash
cd ~/control-room-dsr
git pull origin master
```

### Step 4: Update Nginx Configuration
```bash
# Copy updated nginx config
sudo cp nginx_config.conf /etc/nginx/sites-available/controlroom

# Test nginx configuration
sudo nginx -t

# If test passes, reload nginx
sudo systemctl reload nginx

# Or restart nginx
sudo systemctl restart nginx
```

### Step 5: Restart Flask Application
```bash
# Stop existing gunicorn
pkill gunicorn

# Start fresh gunicorn
nohup gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()" > gunicorn.log 2>&1 &

# Verify it's running
ps aux | grep gunicorn
```

### Step 6: Verify Changes
```bash
# Check nginx config
sudo nginx -T | grep client_max_body_size

# Should show: client_max_body_size 500M;
```

## Test Upload
1. Go to: https://controlroom.prismappolice.in/
2. Login as controlroom user
3. Try uploading large files (up to 500MB)
4. Should work without 413 error

## Configuration Changes Made

### 1. Flask (config.py)
- Changed: `MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB`

### 2. Nginx (nginx_config.conf)
- Changed: `client_max_body_size 500M;`
- Changed: `client_body_buffer_size 256k;`

## Additional Settings (Already in Config)
- Upload timeouts: 300 seconds
- Proxy buffering: disabled for large uploads
- Request buffering: off

## Troubleshooting

### If 413 error persists:
```bash
# Check nginx error log
sudo tail -50 /var/log/nginx/error.log

# Check if config is actually loaded
sudo nginx -T | grep client_max_body_size

# Ensure nginx reloaded properly
sudo systemctl status nginx
```

### If upload still fails:
```bash
# Check gunicorn logs
tail -50 ~/control-room-dsr/gunicorn.log

# Check disk space
df -h
```

## Summary
✅ Flask: 500MB limit
✅ Nginx: 500MB limit  
✅ Timeouts: 300 seconds
✅ Buffering: Optimized for large uploads

All settings synchronized for smooth large file uploads!
