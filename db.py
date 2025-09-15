import sqlite3

DB_NAME = "pos.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        quantity INTEGER
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        total REAL,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )""")
    conn.commit()
    conn.close()

def add_product(name, price, quantity):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    conn.close()

def get_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data

def record_sale(product_id, qty, stock_qty):
    conn = get_connection()
    c = conn.cursor()
    # update stock
    new_qty = stock_qty - qty
    c.execute("UPDATE products SET quantity=? WHERE id=?", (new_qty, product_id))
    # record sale
    c.execute("SELECT price FROM products WHERE id=?", (product_id,))
    price = c.fetchone()[0]
    total = price * qty
    c.execute("INSERT INTO sales (product_id, quantity, total) VALUES (?, ?, ?)", (product_id, qty, total))
    conn.commit()
    conn.close()

def get_sales():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT sales.id, products.name, sales.quantity, sales.total
                 FROM sales JOIN products ON sales.product_id = products.id""")
    data = c.fetchall()
    conn.close()
    return data
