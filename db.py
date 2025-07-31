import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Database Connection Details ---
# These should be the same as your other scripts.
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pyb231273',
    'database': 'think41'
}

def execute_query(query):
    """
    Executes a SQL query and returns the result as a pandas DataFrame.
    Returns a tuple: (data, error_message)
    """
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            # Using pandas to directly read the SQL query results into a DataFrame
            df = pd.read_sql(query, conn)
            return df, None
    except Error as e:
        # Return a specific database error message
        return None, f"Database Error: {e}"
    except Exception as e:
        # Return a general error message for issues like invalid query syntax
        return None, f"An error occurred: {e}"
    finally:
        if conn and conn.is_connected():
            conn.close()

# --- Streamlit App Layout ---

# Set the title of the dashboard
st.set_page_config(page_title="Think41 Database Query Tool", layout="wide")
st.title("🗃️ Think41 Database Query Tool")
st.write("Enter a SQL query below to retrieve data from the `think41` database.")

# --- Sample Queries Section ---
with st.expander("Click to see sample queries"):
    st.code("""
-- Show the 5 most expensive products
SELECT name, brand, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 5;

-- Count the number of orders per status
SELECT status, COUNT(order_id) as number_of_orders
FROM orders
GROUP BY status;

-- Find users from a specific state
SELECT first_name, last_name, email, city, state
FROM users
WHERE state = 'California'
LIMIT 10;
    """, language="sql")


# --- User Input Section ---
# Create a text area for the user to input their SQL query
query_input = st.text_area("SQL Query", height=150, placeholder="SELECT * FROM products LIMIT 10;")

# Create a button to execute the query
if st.button("Run Query"):
    if query_input:
        # Show a spinner while the query is running
        with st.spinner("Executing query..."):
            results_df, error = execute_query(query_input)

        if error:
            # If there was an error, display it in an error box
            st.error(error)
        elif results_df is not None:
            if results_df.empty:
                # If the query ran but returned no results
                st.warning("Query executed successfully, but returned no results.")
            else:
                # If results are returned, display them
                st.success(f"Query returned {len(results_df)} rows.")
                # Display the results in an interactive table
                st.dataframe(results_df)
    else:
        # If the user clicks the button with no query entered
        st.warning("Please enter a SQL query.")
