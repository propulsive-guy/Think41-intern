import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Database Connection Details ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pyb231273',
    'database': 'think41'
}

# --- Caching Database Calls for Performance ---
# This tells Streamlit to cache the results of these functions, so it doesn't
# re-run the same database query every time the user interacts with the app.

@st.cache_data(ttl=600) # Cache data for 10 minutes
def get_departments():
    """Fetches all unique department names from the database."""
    try:
        with mysql.connector.connect(**db_config) as conn:
            query = "SELECT name FROM departments ORDER BY name ASC"
            df = pd.read_sql(query, conn)
            # Return a list of department names
            return df['name'].tolist()
    except Error as e:
        st.error(f"Database Error: {e}")
        return []

@st.cache_data(ttl=60) # Cache data for 1 minute
def get_products(department_name=None):
    """
    Fetches products from the database.
    If a department_name is provided, it fetches products only for that department.
    Otherwise, it fetches all products.
    """
    try:
        with mysql.connector.connect(**db_config) as conn:
            if department_name and department_name != "All Products":
                # Query for a specific department
                query = "SELECT id, name, brand, retail_price, category FROM products WHERE department = %s"
                df = pd.read_sql(query, conn, params=(department_name,))
            else:
                # Query for all products
                query = "SELECT id, name, brand, retail_price, category, department FROM products LIMIT 500" # Limit for performance
                df = pd.read_sql(query, conn)
            return df
    except Error as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()


# --- Streamlit App Layout ---

st.set_page_config(page_title="Think41 E-commerce", layout="wide")

# --- Sidebar for Department Navigation ---
st.sidebar.title("Departments")
departments = ["All Products"] + get_departments()

# Using radio buttons for department selection mimics a navigation menu.
# The `st.session_state` object is used to keep track of the selected department
# across user interactions, simulating URL routing.
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = "All Products"

# Update the selected department in the session state when a new one is clicked.
selected_department = st.sidebar.radio(
    "Select a Department",
    departments,
    index=departments.index(st.session_state.selected_department)
)
st.session_state.selected_department = selected_department


# --- Main Page Content ---

# Fetch the products based on the selected department
products_df = get_products(st.session_state.selected_department)

# --- Department Header ---
if st.session_state.selected_department == "All Products":
    st.title("🛍️ All Products")
    st.write(f"Showing all available products. (Displaying up to 500)")
else:
    st.title(f"🛍️ {st.session_state.selected_department}")
    # Display the product count for the selected department
    st.write(f"Found **{len(products_df)}** products in this department.")

st.markdown("---")


# --- Department Page (Product Display) ---
if not products_df.empty:
    # Display the products in a clean, interactive table
    st.dataframe(
        products_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("Product ID"),
            "name": st.column_config.TextColumn("Product Name", width="large"),
            "brand": st.column_config.TextColumn("Brand"),
            "retail_price": st.column_config.NumberColumn(
                "Price",
                format="$%.2f"
            ),
            "category": st.column_config.TextColumn("Category")
        }
    )
else:
    # Show a message if no products are found for the selected department
    st.warning("No products found for this department.")

