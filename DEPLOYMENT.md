# Control Room DSR - Deployment Guide

## Database Configuration

This application uses **PostgreSQL** database (SQLite has been removed).

### Local Development

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Install and set password for `postgres` user

2. **Create Database and User**
   ```sql
   CREATE DATABASE control_room_dsr;
   CREATE USER dsr_user WITH PASSWORD 'dsr_pass123';
   GRANT ALL PRIVILEGES ON DATABASE control_room_dsr TO dsr_user;
   ```

3. **Configure Environment Variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env with your database credentials
   DATABASE_TYPE=postgresql
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=control_room_dsr
   POSTGRES_USER=dsr_user
   POSTGRES_PASSWORD=dsr_pass123
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   python run.py
   ```

### Cloud Deployment

#### Option 1: Render (Recommended - Free Tier Available)

1. **Create Account**: https://render.com
2. **Create PostgreSQL Database**
   - Go to Dashboard → New → PostgreSQL
   - Note the connection details
3. **Create Web Service**
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn run:app`
4. **Set Environment Variables**
   ```
   DATABASE_TYPE=postgresql
   POSTGRES_HOST=<from-render-database>
   POSTGRES_PORT=5432
   POSTGRES_DB=<from-render-database>
   POSTGRES_USER=<from-render-database>
   POSTGRES_PASSWORD=<from-render-database>
   SECRET_KEY=<generate-random-key>
   ```

#### Option 2: Railway.app

1. **Create Account**: https://railway.app
2. **New Project** → Deploy from GitHub
3. **Add PostgreSQL Plugin**
4. **Environment variables auto-configured**
5. **Deploy automatically**

#### Option 3: DigitalOcean App Platform

1. **Create Managed PostgreSQL Database**
2. **Create App from GitHub**
3. **Link Database**
4. **Set environment variables**
5. **Deploy**

#### Option 4: AWS (Advanced)

1. **RDS PostgreSQL** - Create database instance
2. **EC2 or Elastic Beanstalk** - Deploy Flask app
3. **S3** - Store uploaded files
4. **Configure security groups and VPC**

### Environment Variables for Production

```bash
DATABASE_TYPE=postgresql
POSTGRES_HOST=<your-cloud-db-host>
POSTGRES_PORT=5432
POSTGRES_DB=control_room_dsr
POSTGRES_USER=<your-db-user>
POSTGRES_PASSWORD=<secure-password>
SECRET_KEY=<generate-random-secret-key>
FLASK_ENV=production
FLASK_DEBUG=0
```

### Database Migration

If migrating from SQLite to PostgreSQL:

```bash
# Export data from SQLite
python export_sqlite_data.py

# Import to PostgreSQL
python import_to_postgresql.py
```

### Default Users

After first run, default users will be created:
- **admin** / admin123 (Admin user)
- **controlroom** / controlroom123 (Control room)
- **district users** / {district}_123 (28 districts)

**⚠️ Change passwords immediately after deployment!**

### Features

✅ 32 Users (Admin + Control Room + 30 Districts)
✅ 16 DSR Forms
✅ File Upload System
✅ Excel Export
✅ Date-wise Reports
✅ User Management
✅ Password Management
✅ Mobile Responsive Design

### Support

For issues or questions, check the GitHub repository.
