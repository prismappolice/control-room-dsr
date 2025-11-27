# Fix 413 Error and Open Button Issue - Deployment Guide

## Problems Fixed:
1. **413 Request Entity Too Large** - Nginx upload limit too small
2. **Open button downloading files** - Nginx configuration missing proper MIME types

## Solution Steps:

### Step 1: Update Nginx Configuration

```bash
# SSH to cloud server
ssh prismappolice@control-room-dsr

# Edit Nginx config
sudo nano /etc/nginx/sites-available/controlroom
```

**Add or update these lines in your server block:**

```nginx
server {
    listen 80;
    server_name controlroom.prismappolice.in;

    # Fix 413 error - Increase upload size to 100MB
    client_max_body_size 100M;
    client_body_buffer_size 128k;
    
    # Timeouts for large uploads
    client_body_timeout 300s;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Don't buffer large uploads
        proxy_request_buffering off;
    }
}
```

### Step 2: Test and Reload Nginx

```bash
# Test configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx

# Or restart if needed
sudo systemctl restart nginx
```

### Step 3: Update Flask Code

```bash
# Go to project directory
cd ~/control-room-dsr

# Pull latest code
git pull origin master

# Restart Gunicorn
pkill gunicorn
nohup gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()" > gunicorn.log 2>&1 &
```

### Step 4: Verify

1. **Test large file upload**: Upload file > 16MB
2. **Test Open button**: Click Open - should view in browser, not download
3. **Test Download button**: Should download file

## Quick Fix Commands (All in One):

```bash
# Edit Nginx config
sudo nano /etc/nginx/sites-available/controlroom

# Add these lines under server_name:
#   client_max_body_size 100M;
#   client_body_buffer_size 128k;
#   proxy_request_buffering off;

# Test and reload
sudo nginx -t && sudo systemctl reload nginx

# Update code
cd ~/control-room-dsr
git pull
pkill gunicorn
nohup gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()" > gunicorn.log 2>&1 &
```

## Troubleshooting:

### If 413 error persists:
```bash
# Check Nginx error log
sudo tail -50 /var/log/nginx/error.log

# Increase size further if needed
sudo nano /etc/nginx/nginx.conf
# Add in http block: client_max_body_size 100M;
```

### If Open still downloads:
Check Flask route has `as_attachment=False` in `send_file()`

## Changes Made:
- ✅ config.py: MAX_CONTENT_LENGTH = 100MB
- ✅ Nginx: client_max_body_size = 100MB
- ✅ Nginx: proxy_request_buffering = off
- ✅ Flask routes: view_upload uses as_attachment=False
