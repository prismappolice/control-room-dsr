#!/usr/bin/env python3
"""Complete PostgreSQL Status and Fix"""

# Set environment to PostgreSQL
import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User, DSREntry, ControlRoomUpload
import psycopg2

app = create_app()

def check_postgresql_status():
    """Check PostgreSQL status comprehensively"""
    
    print("🔍 Comprehensive PostgreSQL Status Check")
    print("=" * 50)
    
    with app.app_context():
        # Check database configuration
        print(f"📋 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        try:
            # Direct PostgreSQL connection
            print("\n🔌 Direct PostgreSQL Connection:")
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='control_room_dsr',
                user='dsr_user',
                password='dsr_pass123'
            )
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("""
                SELECT table_name, 
                       (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns
                FROM information_schema.tables t
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            print(f"📋 PostgreSQL Tables:")
            for table, col_count in tables:
                cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
                row_count = cursor.fetchone()[0]
                print(f"   - {table}: {row_count} rows, {col_count} columns")
            
            # Check user table specifically
            cursor.execute('SELECT username, user_type FROM "user" LIMIT 3')
            users = cursor.fetchall()
            print(f"\n👤 Sample users from PostgreSQL:")
            for user in users:
                print(f"   - {user[0]} ({user[1]})")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Direct PostgreSQL error: {e}")
        
        try:
            # Flask SQLAlchemy connection
            print(f"\n🌐 Flask SQLAlchemy Connection:")
            
            # Try to query users through Flask
            user_count = User.query.count()
            print(f"✅ Flask can see {user_count} users")
            
            if user_count > 0:
                admin_user = User.query.filter_by(username='admin').first()
                if admin_user:
                    print(f"✅ Admin user found via Flask: {admin_user.username}")
                else:
                    print("❌ Admin user not found via Flask")
            else:
                print("⚠️  Flask sees empty user table")
                
                # Check if tables exist in Flask
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                flask_tables = inspector.get_table_names()
                print(f"📋 Tables Flask can see: {flask_tables}")
                
        except Exception as e:
            print(f"❌ Flask SQLAlchemy error: {e}")
            
            # If Flask can't see the data, create tables and migrate
            print("\n🔧 Creating Flask tables...")
            db.create_all()
            
            print("📊 Migrating data to Flask tables...")
            # Direct migration from existing PostgreSQL data
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    port='5432', 
                    database='control_room_dsr',
                    user='dsr_user',
                    password='dsr_pass123'
                )
                cursor = conn.cursor()
                
                # Get users from PostgreSQL
                cursor.execute('SELECT id, username, password_hash, user_type, district_name FROM "user"')
                pg_users = cursor.fetchall()
                
                # Add users to Flask
                for user_data in pg_users:
                    existing = User.query.filter_by(username=user_data[1]).first()
                    if not existing:
                        user = User(
                            username=user_data[1],
                            password_hash=user_data[2],
                            user_type=user_data[3],
                            district_name=user_data[4]
                        )
                        db.session.add(user)
                
                db.session.commit()
                print(f"✅ Migrated {len(pg_users)} users to Flask tables")
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                print(f"❌ Migration error: {e}")

if __name__ == '__main__':
    check_postgresql_status()