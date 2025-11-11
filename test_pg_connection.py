#!/usr/bin/env python3
"""Test PostgreSQL connection"""

try:
    import psycopg2
    
    # Try to connect to PostgreSQL
    conn = psycopg2.connect(
        host='localhost',
        database='control_room_dsr', 
        user='dsr_user',
        password='dsr_pass123'
    )
    
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM "user"')
    user_count = cur.fetchone()[0]
    
    print(f"✅ PostgreSQL Connection: SUCCESS")
    print(f"✅ Users in PostgreSQL database: {user_count}")
    
    # Check if data exists
    cur.execute('SELECT username, user_type FROM "user" LIMIT 5')
    users = cur.fetchall()
    print(f"✅ Sample users:")
    for user in users:
        print(f"   - {user[0]} ({user[1]})")
    
    conn.close()
    print(f"✅ PostgreSQL is ready and has migrated data!")
    
except ImportError:
    print(f"❌ psycopg2 not installed. Installing...")
    
except psycopg2.OperationalError as e:
    print(f"❌ PostgreSQL connection failed: {e}")
    print(f"❌ Database might not be set up yet")
    
except Exception as e:
    print(f"❌ Error: {e}")