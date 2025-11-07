"""
PostgreSQL Setup and Database Creation Script
This script helps set up PostgreSQL for the Control Room DSR system
"""

import subprocess
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from pathlib import Path

class PostgreSQLSetup:
    """PostgreSQL setup and database creation"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'control_room_dsr',
            'username': 'dsr_user',
            'password': 'dsr_pass123'
        }
        self.admin_config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'postgres',  # Default PostgreSQL database
            'username': 'postgres',
            'password': ''  # Will be set during installation
        }
    
    def check_postgresql_installed(self):
        """Check if PostgreSQL is installed"""
        try:
            result = subprocess.run(['psql', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PostgreSQL is installed: {result.stdout.strip()}")
                return True
            else:
                print("❌ PostgreSQL not found")
                return False
        except FileNotFoundError:
            print("❌ PostgreSQL not installed")
            return False
    
    def install_postgresql_windows(self):
        """Guide for PostgreSQL installation on Windows"""
        print("\n🔧 PostgreSQL Installation Guide for Windows:")
        print("=" * 50)
        print("1. Download PostgreSQL from: https://www.postgresql.org/download/windows/")
        print("2. Choose the latest stable version (15.x or 16.x)")
        print("3. Run the installer as Administrator")
        print("4. During installation:")
        print("   - Set postgres user password (remember this!)")
        print("   - Default port: 5432 (keep default)")
        print("   - Default data directory (keep default)")
        print("   - Install pgAdmin 4 (recommended)")
        print("5. Add PostgreSQL bin directory to PATH:")
        print("   - Usually: C:\\Program Files\\PostgreSQL\\15\\bin")
        print("6. Restart command prompt after installation")
        print("\n📝 Alternative - Docker Installation:")
        print("docker run --name postgres-dsr -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15")
        print("\n🔄 After installation, run this script again!")
        
    def connect_to_postgres(self, use_admin=True):
        """Connect to PostgreSQL server"""
        config = self.admin_config if use_admin else self.db_config
        
        try:
            # Get password if not set
            if not config['password']:
                config['password'] = input(f"Enter password for {config['username']}: ")
            
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['username'],
                password=config['password']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print(f"✅ Connected to PostgreSQL as {config['username']}")
            return conn
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None
    
    def create_database_and_user(self):
        """Create database and user for DSR system"""
        print("\n🗄️  Creating database and user...")
        
        conn = self.connect_to_postgres(use_admin=True)
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Create user
            cursor.execute(f"SELECT 1 FROM pg_user WHERE usename = '{self.db_config['username']}'")
            if not cursor.fetchone():
                cursor.execute(f"""
                    CREATE USER {self.db_config['username']} 
                    WITH PASSWORD '{self.db_config['password']}'
                """)
                print(f"✅ User '{self.db_config['username']}' created")
            else:
                print(f"ℹ️  User '{self.db_config['username']}' already exists")
            
            # Create database
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_config['database']}'")
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {self.db_config['database']} OWNER {self.db_config['username']}")
                print(f"✅ Database '{self.db_config['database']}' created")
            else:
                print(f"ℹ️  Database '{self.db_config['database']}' already exists")
            
            # Grant privileges
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {self.db_config['database']} TO {self.db_config['username']}")
            print("✅ Privileges granted")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            if conn:
                conn.close()
            return False
    
    def test_connection(self):
        """Test connection to the created database"""
        print("\n🔌 Testing database connection...")
        
        conn = self.connect_to_postgres(use_admin=False)
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                print(f"✅ Connection successful!")
                print(f"📊 PostgreSQL version: {version}")
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                print(f"❌ Connection test failed: {e}")
                return False
        return False
    
    def create_tables_from_sqlite_structure(self):
        """Create tables in PostgreSQL based on SQLite structure"""
        print("\n📋 Creating tables from SQLite structure...")
        
        # Load exported structure
        structure_file = Path(__file__).parent / 'migration_data' / 'table_structures.json'
        if not structure_file.exists():
            print("❌ Table structure file not found. Run export script first.")
            return False
        
        with open(structure_file, 'r') as f:
            structures = json.load(f)
        
        conn = self.connect_to_postgres(use_admin=False)
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # SQL type mapping from SQLite to PostgreSQL
            type_mapping = {
                'INTEGER': 'SERIAL',
                'VARCHAR(80)': 'VARCHAR(80)',
                'VARCHAR(120)': 'VARCHAR(120)',
                'VARCHAR(20)': 'VARCHAR(20)',
                'VARCHAR(100)': 'VARCHAR(100)',
                'VARCHAR(50)': 'VARCHAR(50)',
                'VARCHAR(255)': 'VARCHAR(255)',
                'VARCHAR(500)': 'VARCHAR(500)',
                'BOOLEAN': 'BOOLEAN',
                'DATETIME': 'TIMESTAMP',
                'DATE': 'DATE',
                'TEXT': 'TEXT'
            }
            
            for table_name, columns in structures.items():
                # Build CREATE TABLE statement
                col_definitions = []
                
                for col in columns:
                    col_name = col['name']
                    col_type = type_mapping.get(col['type'], col['type'])
                    
                    # Handle primary key
                    if col['primary_key'] and col_type == 'SERIAL':
                        col_def = f"{col_name} SERIAL PRIMARY KEY"
                    else:
                        col_def = f"{col_name} {col_type}"
                        
                        # Handle NOT NULL
                        if col['notnull']:
                            col_def += " NOT NULL"
                        
                        # Handle default values
                        if col['default_value']:
                            col_def += f" DEFAULT {col['default_value']}"
                    
                    col_definitions.append(col_def)
                
                create_sql = f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        {', '.join(col_definitions)}
                    )
                """
                
                cursor.execute(create_sql)
                print(f"✅ Table '{table_name}' created")
            
            cursor.close()
            conn.close()
            print("✅ All tables created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Table creation failed: {e}")
            if conn:
                conn.close()
            return False
    
    def save_connection_info(self):
        """Save PostgreSQL connection info for the application"""
        config_info = {
            'DATABASE_TYPE': 'postgresql',
            'POSTGRES_HOST': self.db_config['host'],
            'POSTGRES_PORT': self.db_config['port'],
            'POSTGRES_DB': self.db_config['database'],
            'POSTGRES_USER': self.db_config['username'],
            'POSTGRES_PASSWORD': self.db_config['password'],
            'SQLALCHEMY_DATABASE_URI': f"postgresql://{self.db_config['username']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        }
        
        config_file = Path(__file__).parent / 'postgresql_config.json'
        with open(config_file, 'w') as f:
            json.dump(config_info, f, indent=2)
        
        print(f"📁 Connection info saved to {config_file}")
        
        # Create environment setup script
        env_script = f"""# PostgreSQL Environment Setup
# Copy these lines to your environment or .env file

export DATABASE_TYPE=postgresql
export POSTGRES_HOST={self.db_config['host']}
export POSTGRES_PORT={self.db_config['port']}
export POSTGRES_DB={self.db_config['database']}
export POSTGRES_USER={self.db_config['username']}
export POSTGRES_PASSWORD={self.db_config['password']}

# For Windows PowerShell:
$env:DATABASE_TYPE="postgresql"
$env:POSTGRES_HOST="{self.db_config['host']}"
$env:POSTGRES_PORT="{self.db_config['port']}"
$env:POSTGRES_DB="{self.db_config['database']}"
$env:POSTGRES_USER="{self.db_config['username']}"
$env:POSTGRES_PASSWORD="{self.db_config['password']}"
"""
        
        env_file = Path(__file__).parent / 'postgresql_setup.env'
        with open(env_file, 'w') as f:
            f.write(env_script)
        
        print(f"🔧 Environment setup saved to {env_file}")
        return config_info

def main():
    """Main setup function"""
    setup = PostgreSQLSetup()
    
    print("🚀 PostgreSQL Setup for Control Room DSR")
    print("=" * 45)
    
    # Check if PostgreSQL is installed
    if not setup.check_postgresql_installed():
        setup.install_postgresql_windows()
        return False
    
    # Create database and user
    if not setup.create_database_and_user():
        print("❌ Failed to create database and user")
        return False
    
    # Test connection
    if not setup.test_connection():
        print("❌ Failed to connect to database")
        return False
    
    # Create tables
    if not setup.create_tables_from_sqlite_structure():
        print("❌ Failed to create tables")
        return False
    
    # Save configuration
    config = setup.save_connection_info()
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run data import script to migrate data")
    print("2. Test application with PostgreSQL")
    print("3. Update environment variables if needed")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Setup incomplete. Please install PostgreSQL first.")
        sys.exit(1)