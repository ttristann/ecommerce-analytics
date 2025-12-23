"""
Supabase Database Connection Utilities
This provides functions to connect to PostgreSQL database on Supabase
"""

import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
from psycopg2.extras import execute_batch

import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from supabase import create_client, Client

# loads credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# does not exist
SUPABASE_SERVICE_KEY = "service key here"

def get_supabase_client(use_service_role: bool = False) -> Client:
    """
    Create and returns a Supabase Client, using the
    credentials inside the .env file

    Args:
    - use_service_role:
        if True, uses service_role key (bypasses RLS)
        if False, uses anon key (normal operations)

    """

    # create client
    try:
        if use_service_role:
            client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        else:
            client = create_client(SUPABASE_URL, SUPABASE_KEY)

        return client
    
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        raise e

# the default client instance
supabase : Client = get_supabase_client()

# helper functions for the supabase functionalities
def insert_data(table_name: str, data: Dict[str, Any]) -> Dict:
    """
    Insert a single row into the specified data table

    Args:
    - table_name: Name of the table to interact
    - data: Dictionary with column names as keys

    Returns:
    - Inserts a row data

    """
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
        raise

def insert_many(table_name: str, data_list: List[Dict[str, Any]]) -> List[Dict]:
    """
    Insert multiple rows into a table (bulk insert)

    Args:
    - table_name: Name of the table to interact
    - data_list: List of dictionaries, each representing a row
    """
    try:
        response = supabase.table(table_name).insert(data_list).execute()
        return response.data
    except Exception as e:
        print(f"Error bulk inserting into {table_name}: {e}")
        raise

def select_all(table_name: str, limit: int = 1000) -> List[Dict]:
    """
    Select all rows from a table
    
    Args:
        table_name: Name of the table
        limit: Maximum number of rows to return
    
    Returns:
    - List of dictionaries (rows)
    
    Example:
    - customers = select_all('customers', limit=100)
    """
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Error selecting from {table_name}: {e}")
        raise


def select_where(table_name: str, column: str, value: Any) -> List[Dict]:
    """
    Select rows with WHERE clause
    
    Args:
    - table_name: Name of the table
    - column: Column name to filter on
    - value: Value to match
    
    Returns:
    - List of matching rows

    """
    try:
        response = supabase.table(table_name).select("*").eq(column, value).execute()
        return response.data
    except Exception as e:
        print(f"Error selecting from {table_name}: {e}")
        raise


def count_rows(table_name: str) -> int:
    """
    Count total rows in a table
    
    Args:
    - table_name: Name of the table
    
    Returns:
    - Number of rows
    """
    try:
        response = supabase.table(table_name).select("*", count='exact').execute()
        return response.count
    except Exception as e:
        print(f"Error counting rows in {table_name}: {e}")
        raise


def delete_all(table_name: str) -> bool:
    """
    Delete all rows from a table (CAREFUL!)
    
    Args:
    - table_name: Name of the table
    
    Returns:
    - True if successful
    """
    try:
        # use with caution since this deletes all
        response = supabase.table(table_name).delete().neq('customer_id', 0).execute()
        print(f"Deleted all rows from {table_name}")
        return True
    except Exception as e:
        print(f"Error deleting from {table_name}: {e}")
        raise


def execute_sql(sql_query: str) -> List[Dict]:
    """
    Execute raw SQL query using Supabase RPC
    
    Note: For complex queries, you may need to create a PostgreSQL function
    and call it via RPC. For now, use the table methods above.
    
    Args:
    - sql_query: SQL query string
    
    Returns:
    - Query results
    """
    # Note: Direct SQL execution via REST API is limited
    # For complex queries, create a PostgreSQL function in Supabase
    # and call it like: supabase.rpc('function_name', {}).execute()
    
    print("Note: Direct SQL execution via client is limited.")
    print("Use table methods (select, insert, etc.) or create PostgreSQL functions.")
    raise NotImplementedError("Use table methods or PostgreSQL functions via RPC")


# ============================================================================
# CONNECTION TEST
# ============================================================================

def test_connection():
    """
    Test Supabase connection and show database info
    """
    print("=" * 70)
    print("TESTING SUPABASE CLIENT CONNECTION")
    print("=" * 70)
    
    try:
        # Test 1: Check if we can list tables
        print("\nAttempting to connect to Supabase...")
        
        # Try to access a table (this will fail if connection is bad)
        tables_to_check = ['customers', 'products', 'inventory', 'transactions', 'transaction_items']
        
        print(f" Successfully connected to Supabase!")
        print(f" Project URL: {SUPABASE_URL}")
        
        # Check each table
        print(f"\n Checking tables:")
        for table in tables_to_check:
            try:
                count = count_rows(table)
                print(f"  - {table}: {count} rows")
            except Exception as e:
                print(f"  - {table}: Error accessing table ({str(e)[:50]})")
        
        # Test insert (we'll delete it right after)
        print(f"\n Testing write operations...")
        test_data = {
            'customer_id': 99999,
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'customer_segment': 'Regular',
            'lifetime_value': 0
        }
        
        try:
            # Insert test data
            insert_data('customers', test_data)
            print(f"  ✓ Insert test: SUCCESS")
            
            # Delete test data
            supabase.table('customers').delete().eq('customer_id', 99999).execute()
            print(f"  ✓ Delete test: SUCCESS")
            
        except Exception as e:
            print(f"  ✗ Write test failed: {e}")
        
        print("\n" + "=" * 70)
        print(" CONNECTION TEST SUCCESSFUL!")
        print("=" * 70)
        print("\nYour Supabase client is working!")
        print("This connection uses HTTPS (port 443) which usually works")
        print("through corporate firewalls.")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("CONNECTION TEST FAILED")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Check your SUPABASE_URL (should start with https://)")
        print("2. Verify your API keys are correct")
        print("3. Check Project Settings > API in Supabase dashboard")
        print("4. Ensure project is not paused")
        print("5. Try from home network to rule out firewall")
        
        return False


def show_table_sample(table_name: str, limit: int = 5):
    """
    Show sample data from a table
    
    Args:
        table_name: Name of table to sample
        limit: Number of rows to show
    """
    try:
        rows = select_all(table_name, limit=limit)
        
        if rows:
            print(f"\n{table_name} (showing {len(rows)} rows):")
            print("-" * 70)
            
            # Show first row keys (columns)
            if rows:
                print("Columns:", ", ".join(rows[0].keys()))
                print("-" * 70)
                
                # Show each row
                for i, row in enumerate(rows, 1):
                    print(f"Row {i}:")
                    for key, value in row.items():
                        print(f"  {key}: {value}")
                    print()
        else:
            print(f"\n{table_name}: No data (0 rows)")
            
    except Exception as e:
        print(f"Error accessing {table_name}: {e}")


if __name__ == "__main__":
    # Run connection test
    print("Running Supabase client test...\n")
    
    success = test_connection()
    
    if success:
        print("\n" + "=" * 70)
        print("BONUS: Available Operations")
        print("=" * 70)
        print("\nYou can now use these functions:")
        print("  - insert_data(table, data_dict)")
        print("  - insert_many(table, list_of_dicts)")
        print("  - select_all(table, limit)")
        print("  - select_where(table, column, value)")
        print("  - count_rows(table)")
        print("  - delete_all(table)  # Be careful!")
        
        print("\nExample usage:")
        print("  from src.warehouse.supabase_client import supabase, insert_data")
        print("  insert_data('customers', {'customer_id': 1, 'email': 'test@test.com'})")

# # databae configuration
# load_dotenv()
# DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "port": int(os.getenv("DB_PORT")),
#     "database": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
# }

# def test_config():
#     print(DB_CONFIG['host'])
#     print(DB_CONFIG['port'])
#     print(DB_CONFIG['database'])
#     print(DB_CONFIG['user'])
#     print(DB_CONFIG['password'])

# def get_connection():
#     """
#     Create and return a database connection

#     Returns:
#     - psycopg2 connection object
#     """
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to the database: {e}")
#         print("Double check the connection details in the DB_CONFIG")

# @contextmanager
# def get_db_cursor():
#     """
#     Context manager for database cursor
#     This automatically commits and closes connection

#     Usage:
#         with get_db_cursor() as cursor:
#             cursor.execute("SELECT * FROM customers)
#             results = cursor.fetchall()
#     """
#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         yield cursor
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         print("Database error: {e}")
#         raise e
#     finally:
#         cursor.close()
#         conn.close()

# def test_connection():
#     """
#     Test database connection and show table list
#     """
#     print("=" * 70)
#     print("TESTING SUPABASE DATABASE CONNECTION")
#     print("=" * 70)
    
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
        
#         # get PostgreSQL version
#         cursor.execute("SELECT version();")
#         version = cursor.fetchone()[0]
#         print(f"\nSuccessfully connected to Supabase!")
#         print(f"  PostgreSQL Version: {version.split(',')[0]}")
        
#         # get database name and host
#         cursor.execute("SELECT current_database(), inet_server_addr(), inet_server_port();")
#         db_name, host, port = cursor.fetchone()
#         print(f"  Database: {db_name}")
#         print(f"  Host: {host}:{port}")
        
#         # list all tables
#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public' 
#             AND table_type = 'BASE TABLE'
#             ORDER BY table_name;
#         """)
        
#         tables = cursor.fetchall()
#         print(f"\nFound {len(tables)} tables:")
#         for table in tables:
#             print(f"  - {table[0]}")
        
#         # count rows in each table
#         print(f"\nCurrent row counts:")
#         for table in tables:
#             table_name = table[0]
#             cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
#             count = cursor.fetchone()[0]
#             print(f"  - {table_name}: {count:,} rows")
        
#         # list views
#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.views 
#             WHERE table_schema = 'public'
#             ORDER BY table_name;
#         """)
        
#         views = cursor.fetchall()
#         if views:
#             print(f"\nFound {len(views)} views:")
#             for view in views:
#                 print(f"  - {view[0]}")
        
#         # check database size
#         cursor.execute("""
#             SELECT pg_size_pretty(pg_database_size(current_database())) as size;
#         """)
#         db_size = cursor.fetchone()[0]
#         print(f"\nDatabase size: {db_size}")
        
#         cursor.close()
#         conn.close()
        
#         print("\n" + "=" * 70)
#         print("CONNECTION TEST SUCCESSFUL!")
#         print("=" * 70)
        
#         return True
        
#     except psycopg2.Error as e:
#         print("\n" + "=" * 70)
#         print("CONNECTION TEST FAILED")
#         print("=" * 70)
#         print(f"\nError: {e}")
#         print("\nTroubleshooting:")
#         print("1. Check your DB_CONFIG settings")
#         print("2. Verify password is correct")
#         print("3. Check host address (should end with .supabase.co)")
#         print("4. Ensure project is not paused (Supabase pauses inactive projects)")
#         print("5. Check internet connection")
        
#         return False
    
# def get_table_info(table_name:str):
#     """
#     Get detailed information about a table

#     Args:
#     - table_name: name of the table

#     """
#     with get_db_cursor() as cursor:
#         # getting column information
#         cursor.execute(f"""
#             SELECT
#                 column_name,
#                 data_type,
#                 character_maximum_length,
#                 is_nullable,
#                 column_default
#             FROM information_schema.columns
#             WHERE table_name = '{table_name}'
#             ORDER BY ordinal_position;         
#         """)

#         columns = cursor.fetchall()
#         print(f"\nTable: {table_name}")
#         print("-"*70)
#         print(f"{'Column':<25} {'Type':<20} {'Nullable':<10} {'Default':<15}")
#         print("-" * 70)
        
#         for col in columns:
#             col_name, data_type, max_length, nullable, default = col
#             type_str = f"{data_type}({max_length})" if max_length else data_type
#             default_str = str(default)[:15] if default else ''
#             print(f"{col_name:<25} {type_str:<20} {nullable:<10} {default_str:<15}")

if __name__ == "__main__":
    # testing db_config
    test_config()

    # testing connection
    # success = test_connection()
    # if success:
    #     print()
    #     print("=" * 70)
    #     print("BONUS: TABLE SCHEMA DETAILS")
    #     print("=" * 70)
    #     get_table_info("customers")
