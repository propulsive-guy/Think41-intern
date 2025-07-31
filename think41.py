import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

def upload_csv_to_mysql():
    """
    Connects to a MySQL database and uploads data from multiple CSV files
    into their corresponding tables, handling duplicates and large files.
    """
    # --- IMPORTANT: UPDATE THIS PATH ---
    # Set the absolute path to the directory where your CSV files are stored.
    # Example for Windows: 'C:/Users/YourUser/Downloads/csv_data'
    # Example for macOS/Linux: '/Users/YourUser/Downloads/csv_data'
    csv_directory_path = '/Users/priyanshubehere/Downloads/archive' # <-- CHANGE THIS

    # --- Database Connection Details ---
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'pyb231273',
        'database': 'think41'
    }

    # Mapping of CSV filenames to their corresponding table names.
    table_map = {
        'distribution_centers.csv': 'distribution_centers',
        'users.csv': 'users',
        'products.csv': 'products',
        'inventory_items.csv': 'inventory_items',
        'orders.csv': 'orders',
        'order_items.csv': 'order_items'
    }
    
    # The order in which to load tables to respect foreign key constraints.
    load_order = [
        'distribution_centers.csv',
        'users.csv',
        'products.csv',
        'inventory_items.csv',
        'orders.csv',
        'order_items.csv'
    ]

    conn = None
    try:
        print("Connecting to the MySQL database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connection successful.")

        for csv_file in load_order:
            table_name = table_map.get(csv_file)
            if not table_name:
                continue

            file_path = os.path.join(csv_directory_path, csv_file)

            if not os.path.exists(file_path):
                print(f"\n[WARNING] File not found: {file_path}. Skipping.")
                continue

            print(f"\n--- Processing {csv_file} for table `{table_name}` ---")

            try:
                # Check and re-establish connection if it has been lost
                conn.ping(reconnect=True, attempts=3, delay=5)
                cursor = conn.cursor()

                df = pd.read_csv(file_path)
                df = df.where(pd.notnull(df), None)

                # --- Data Validation and Cleaning ---
                if table_name == 'products':
                    initial_rows = len(df)
                    # Remove rows where the 'name' column is null, as it's a required field
                    df.dropna(subset=['name'], inplace=True)
                    if len(df) < initial_rows:
                        print(f"[INFO] Skipped {initial_rows - len(df)} rows from products.csv due to empty 'name'.")
                
                if df.empty:
                    print("[INFO] No data to upload after cleaning. Skipping.")
                    continue

                # --- SQL Statement Construction ---
                cols = ", ".join([f"`{c}`" for c in df.columns])
                placeholders = ", ".join(["%s"] * len(df.columns))
                
                # Create the 'ON DUPLICATE KEY UPDATE' part of the query
                # This updates the row with new values if a duplicate primary/unique key is found
                update_clause = ", ".join([f"`{col}` = VALUES(`{col}`)" for col in df.columns])
                
                sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_clause}"

                # --- Batch/Chunk Processing for Large Files ---
                chunk_size = 1000
                total_rows_affected = 0
                
                for i in range(0, len(df), chunk_size):
                    chunk = df[i:i + chunk_size]
                    data_to_insert = [tuple(row) for row in chunk.itertuples(index=False)]
                    
                    cursor.executemany(sql, data_to_insert)
                    conn.commit()
                    
                    total_rows_affected += cursor.rowcount
                    print(f"  ... processed chunk {i//chunk_size + 1}, {total_rows_affected} total rows affected.")

                print(f"[SUCCESS] Finished loading data into `{table_name}`. Total rows affected: {total_rows_affected}.")

            except Error as e:
                print(f"[ERROR] A database error occurred for table `{table_name}`: {e}")
                conn.rollback() # Roll back changes for the failed table
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred for table `{table_name}`: {e}")

    except Error as e:
        print(f"Error connecting to or interacting with MySQL: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nMySQL connection is closed.")

if __name__ == '__main__':
    upload_csv_to_mysql()
