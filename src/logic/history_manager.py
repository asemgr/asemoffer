import streamlit as st
from datetime import datetime
import pandas as pd
import os
import sqlite3
import json

DB_PATH = os.path.join("data", "offers.db")

# Οι στήλες που θέλουμε να έχει το Excel
EXPECTED_COLUMNS = [
    "Username", "Date_Time", "Customer_Name", "Catalog", 
    "Product", "Product_Price", "Discount", "Offer_Duration"
]

def save_offer(username, items, customer_name="ΓΕΝΙΚΟΣ ΠΕΛΑΤΗΣ", catalog="ΧΟΝΔΡΙΚΗΣ", discount=0.0, duration="30 Ημέρες", **kwargs):
    """Αποθηκεύει την προσφορά στο Excel."""
    if not items:
        return

    try:
        clean_discount = float(discount) if discount is not None else 0.0
    except:
        clean_discount = 0.0

    # Calculate total price
    total_price = 0.0
    # Determine price column based on catalog
    price_col = 'ΤΙΜΗ_Α'
    if str(catalog).upper() == "ΛΙΑΝΙΚΗΣ":
        price_col = 'ΤΙΜΗ_Β'

    for item in items:
        try:
            # Try specific column first, then generic keys
            val = item.get(price_col, item.get('ΤΙΜΗ', item.get('Product_Price', 0)))
            price = float(val) if val is not None else 0.0
            total_price += price
        except:
            pass

    # Serialize items to JSON
    products_json = json.dumps(items)
    timestamp = datetime.now()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO offers (username, timestamp, customer_name, catalog, products_json, total_price, discount, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, timestamp, customer_name, catalog, products_json, total_price, clean_discount, duration))
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης στη βάση δεδομένων: {e}")

def get_user_history(username, role):
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
    try:
        conn = sqlite3.connect(DB_PATH)
        
        query = "SELECT * FROM offers"
        params = []
        
        if str(role).upper() != "ADMIN":
            query += " WHERE LOWER(username) = LOWER(?)"
            params.append(str(username).strip())
            
        query += " ORDER BY timestamp DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if df.empty:
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

        # Rename columns to match UI expectations
        df = df.rename(columns={
            'username': 'Username',
            'timestamp': 'Date_Time',
            'customer_name': 'Customer_Name',
            'catalog': 'Catalog',
            'total_price': 'Product_Price',
            'discount': 'Discount',
            'duration': 'Offer_Duration'
        })

        # Create 'Product' column from 'products_json'
        def parse_products(json_str):
            try:
                items = json.loads(json_str)
                names = [item.get('ΠΡΟΪΟΝ', item.get('Product', 'Unknown')) for item in items]
                return ", ".join(names)
            except:
                return "Error"

        df['Product'] = df['products_json'].apply(parse_products)
        df['Date_Time'] = pd.to_datetime(df['Date_Time'])
        
        return df
    except Exception as e:
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

def get_user_stats(username, role):
    df = get_user_history(username, role)
    
    if df.empty:
        return {
            "total_offers": 0, 
            "total_products": 0,
            "unique_clients": 0,
            "top_product": "N/A"
        }

    total_offers = len(df)
    unique_clients = df['Customer_Name'].nunique()
    
    all_products = []
    if 'products_json' in df.columns:
        for json_str in df['products_json']:
            try:
                items = json.loads(json_str)
                for item in items:
                    all_products.append(item.get('ΠΡΟΪΟΝ', item.get('Product', 'Unknown')))
            except:
                pass
    
    total_products = len(all_products)
    
    top_product = "N/A"
    if all_products:
        from collections import Counter
        top_product = Counter(all_products).most_common(1)[0][0]

    return {
        "total_offers": total_offers,
        "total_products": total_products,
        "unique_clients": unique_clients,
        "top_product": top_product
    }