import sqlite3

conn = sqlite3.connect('instance/control_room_dsr.db')

print('Tables:')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    print(f'- {t[0]}')

print('\nUser table columns:')
try:
    user_cols = conn.execute("PRAGMA table_info(user)").fetchall()
    for c in user_cols:
        print(f'- {c[1]} ({c[2]})')
except:
    print('No user table')

print('\nDSR Entry columns:')
try:
    dsr_cols = conn.execute("PRAGMA table_info(dsr_entry)").fetchall()
    for c in dsr_cols:
        print(f'- {c[1]} ({c[2]})')
except:
    print('No dsr_entry table')

print('\nControl Room Upload columns:')
try:
    upload_cols = conn.execute("PRAGMA table_info(control_room_upload)").fetchall()
    for c in upload_cols:
        print(f'- {c[1]} ({c[2]})')
except:
    print('No control_room_upload table')

conn.close()