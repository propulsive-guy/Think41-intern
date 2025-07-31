following is the schema of the databse 


mysql> create database think41
    -> ;
Query OK, 1 row affected (0.03 sec)

mysql> use think41;
Database changed
mysql> CREATE TABLE IF NOT EXISTS distribution_centers (
    ->     id INT PRIMARY KEY,
    ->     name VARCHAR(255) NOT NULL,
    ->     latitude DECIMAL(9, 6) NOT NULL,
    ->     longitude DECIMAL(9, 6) NOT NULL
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> CREATE TABLE IF NOT EXISTS users (
    ->     id INT PRIMARY KEY,
    ->     first_name VARCHAR(255),
    ->     last_name VARCHAR(255),
    ->     email VARCHAR(255) NOT NULL UNIQUE,
    ->     age INT,
    ->     gender VARCHAR(50),
    ->     state VARCHAR(255),
    ->     street_address VARCHAR(255),
    ->     postal_code VARCHAR(50),
    ->     city VARCHAR(255),
    ->     country VARCHAR(255),
    ->     latitude DECIMAL(9, 6),
    ->     longitude DECIMAL(9, 6),
    ->     traffic_source VARCHAR(255),
    ->     created_at TIMESTAMP NOT NULL
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE TABLE IF NOT EXISTS products (
    ->     id INT PRIMARY KEY,
    ->     cost DECIMAL(10, 2) NOT NULL,
    ->     category VARCHAR(255) NOT NULL,
    ->     name VARCHAR(255) NOT NULL,
    ->     brand VARCHAR(255),
    ->     retail_price DECIMAL(10, 2) NOT NULL,
    ->     department VARCHAR(255) NOT NULL,
    ->     sku VARCHAR(255) NOT NULL UNIQUE,
    ->     distribution_center_id INT NOT NULL,
    -> 
    ->     -- Foreign Key to link with the distribution_centers table
    ->     CONSTRAINT fk_products_distribution_center
    ->         FOREIGN KEY (distribution_center_id) REFERENCES distribution_centers(id)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE TABLE IF NOT EXISTS inventory_items (
    ->     id INT PRIMARY KEY,
    ->     product_id INT NOT NULL,
    ->     created_at TIMESTAMP NOT NULL,
    ->     sold_at TIMESTAMP NULL, -- Can be NULL if the item is not yet sold
    ->     cost DECIMAL(10, 2) NOT NULL,
    ->     product_category VARCHAR(255),
    ->     product_name VARCHAR(255),
    ->     product_brand VARCHAR(255),
    ->     product_retail_price DECIMAL(10, 2),
    ->     product_department VARCHAR(255),
    ->     product_sku VARCHAR(255),
    ->     product_distribution_center_id INT NOT NULL,
    -> 
    ->     -- Foreign Key to link with the products table
    ->     CONSTRAINT fk_inventory_product
    ->         FOREIGN KEY (product_id) REFERENCES products(id),
    ->     -- Foreign Key to link with the distribution_centers table
    ->     CONSTRAINT fk_inventory_distribution_center
    ->         FOREIGN KEY (product_distribution_center_id) REFERENCES distribution_centers(id)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE TABLE IF NOT EXISTS orders (
    ->     order_id INT PRIMARY KEY,
    ->     user_id INT NOT NULL,
    ->     status VARCHAR(50) NOT NULL,
    ->     gender VARCHAR(50),
    ->     created_at TIMESTAMP NOT NULL,
    ->     returned_at TIMESTAMP NULL, -- Can be NULL
    ->     shipped_at TIMESTAMP NULL,   -- Can be NULL
    ->     delivered_at TIMESTAMP NULL, -- Can be NULL
    ->     num_of_item INT NOT NULL,
    -> 
    ->     -- Foreign Key to link with the users table
    ->     CONSTRAINT fk_orders_user
    ->         FOREIGN KEY (user_id) REFERENCES users(id)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> CREATE TABLE IF NOT EXISTS order_items (
    ->     id INT PRIMARY KEY,
    ->     order_id INT NOT NULL,
    ->     user_id INT NOT NULL,
    ->     product_id INT NOT NULL,
    ->     inventory_item_id INT NOT NULL UNIQUE, -- Each inventory item can only be in one order
    ->     status VARCHAR(50) NOT NULL,
    ->     created_at TIMESTAMP NOT NULL,
    ->     shipped_at TIMESTAMP NULL,
    ->     delivered_at TIMESTAMP NULL,
    ->     returned_at TIMESTAMP NULL,
    -> 
    ->     -- Foreign Keys to link with other tables
    ->     CONSTRAINT fk_order_items_order
    ->         FOREIGN KEY (order_id) REFERENCES orders(order_id),
    ->     CONSTRAINT fk_order_items_user
    ->         FOREIGN KEY (user_id) REFERENCES users(id),
    ->     CONSTRAINT fk_order_items_product
    ->         FOREIGN KEY (product_id) REFERENCES products(id),
    ->     CONSTRAINT fk_order_items_inventory_item
    ->         FOREIGN KEY (inventory_item_id) REFERENCES inventory_items(id)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> LOAD DATA INFILE '/path/to/your/csv/file/distribution_centers.csv'
    -> INTO TABLE distribution_centers
    -> FIELDS TERMINATED BY ','
    -> ENCLOSED BY '"'
    -> LINES TERMINATED BY '\n'
    -> fkefwedeIGNORE 1 ROWS;
