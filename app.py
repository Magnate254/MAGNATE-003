import streamlit as st
import sqlite3
from db import init_db, add_product, get_products, record_sale, get_sales

# Initialize database
init_db()

# --- HEADER with Logo ---
st.set_page_config(page_title="ＭＡＧＮＡＴＥ POS", layout="wide")
st.markdown("<h1 style='text-align: center;'>ＭＡＧＮＡＴＥ</h1>", unsafe_allow_html=True)
st.caption("where freedom meets purpose")

# Load Logo
import os
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    st.markdown("### MAGNATE POS")

# Contact Info
st.markdown("""
📍 **Address:** ROVISTA KENYA  
📞 **Phone:** +254 700 000 000  
✉️ **Email:** magnate003@email.com  
🌐 **Website:** www.magnaterovista.com
""")

# --- Sidebar Navigation ---
menu = ["Add Product", "View Products", "New Sale", "View Sales"]
choice = st.sidebar.radio("Navigation", menu)

# --- Add Product ---
if choice == "Add Product":
    st.subheader("➕ Add New Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, step=0.01)
    quantity = st.number_input("Quantity", min_value=0, step=1)

    if st.button("Add Product"):
        add_product(name, price, quantity)
        st.success(f"✅ {name} added successfully!")

# --- View Products ---
elif choice == "View Products":
    st.subheader("📦 Products in Stock")
    products = get_products()
    if products:
        st.table(products)
    else:
        st.info("No products found.")

# --- New Sale ---
elif choice == "New Sale":
    st.subheader("🛒 Record a Sale")
    products = get_products()
    if products:
        product_names = [p[1] for p in products]
        selected = st.selectbox("Select Product", product_names)
        qty = st.number_input("Quantity", min_value=1, step=1)

        if st.button("Record Sale"):
            product = [p for p in products if p[1] == selected][0]
            record_sale(product[0], qty, product[2])
            st.success(f"✅ Sale recorded: {qty} x {selected}")
    else:
        st.warning("No products available. Please add products first.")

# --- View Sales ---
elif choice == "View Sales":
    st.subheader("📑 Sales Records")
    sales = get_sales()
    if sales:
        st.table(sales)
    else:
        st.info("No sales recorded yet.")
