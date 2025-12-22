"""
Supabase Database Connection Utilities
This provides functions to connect to PostgreSQL database on Supabase
"""

import os
import psycopg2
from contextlib import contextmanager
from psycopg2.extras import execute_batch

# databae configuration
DB_CONFIG = {
    'host': 'db.ewwytsmlhruqmnlbakst.supabase.co',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres', 
    'password': 'etlproject123!'
}

def get_connection():
    """
    Create and return a database connection

    Returns:
    - psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        print("Double check the connection details in the DB_CONFIG")

@contextmanager
def get_db_cursor():
    """
    Context manager for database cursor
    This automatically commits and closes connection

    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM customers)
            results = cursor.fetchall()
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Database error: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def test_connection():
    """
    Test database connection and show table list
    """
    print("=" * 70)
    print("TESTING SUPABASE DATABASE CONNECTION")
    print("=" * 70)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\nSuccessfully connected to Supabase!")
        print(f"  PostgreSQL Version: {version.split(',')[0]}")
        
        # get database name and host
        cursor.execute("SELECT current_database(), inet_server_addr(), inet_server_port();")
        db_name, host, port = cursor.fetchone()
        print(f"  Database: {db_name}")
        print(f"  Host: {host}:{port}")
        
        # list all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # count rows in each table
        print(f"\nCurrent row counts:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count:,} rows")
        
        # list views
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        views = cursor.fetchall()
        if views:
            print(f"\nFound {len(views)} views:")
            for view in views:
                print(f"  - {view[0]}")
        
        # check database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size;
        """)
        db_size = cursor.fetchone()[0]
        print(f"\nDatabase size: {db_size}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("CONNECTION TEST SUCCESSFUL!")
        print("=" * 70)
        
        return True
        
    except psycopg2.Error as e:
        print("\n" + "=" * 70)
        print("CONNECTION TEST FAILED")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Check your DB_CONFIG settings")
        print("2. Verify password is correct")
        print("3. Check host address (should end with .supabase.co)")
        print("4. Ensure project is not paused (Supabase pauses inactive projects)")
        print("5. Check internet connection")
        
        return False
    
def get_table_info(table_name:str):
    """
    Get detailed information about a table

    Args:
    - table_name: name of the table

    """
    with get_db_cursor() as cursor:
        # getting column information
        cursor.execute(f"""
            SELECT
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;         
        """)

        columns = cursor.fetchall()
        print(f"\nTable: {table_name}")
        print("-"*70)
        print(f"{'Column':<25} {'Type':<20} {'Nullable':<10} {'Default':<15}")
        print("-" * 70)
        
        for col in columns:
            col_name, data_type, max_length, nullable, default = col
            type_str = f"{data_type}({max_length})" if max_length else data_type
            default_str = str(default)[:15] if default else ''
            print(f"{col_name:<25} {type_str:<20} {nullable:<10} {default_str:<15}")

if __name__ == "__main__":
    # testing connection
    success = test_connection()
    if success:
        print()
        print("=" * 70)
        print("BONUS: TABLE SCHEMA DETAILS")
        print("=" * 70)
        get_table_info("customers")
        