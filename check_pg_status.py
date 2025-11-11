#!/usr/bin/env python3
"""Quick PostgreSQL Status Check"""

import psycopg2

try:
    # Connect to PostgreSQL
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
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"📋 Tables in PostgreSQL: {[t[0] for t in tables]}")
    
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"👥 Users count: {user_count}")
    
    if user_count > 0:
        cursor.execute("SELECT username, user_type FROM users LIMIT 3")
        sample_users = cursor.fetchall()
        print("👤 Sample users:")
        for user in sample_users:
            print(f"   - {user[0]} ({user[1]})")
    
    cursor.close()
    conn.close()
    
    print("✅ PostgreSQL is working and has your data!")

except Exception as e:
    print(f"❌ Error: {e}")