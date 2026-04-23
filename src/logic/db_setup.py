import sqlite3
import os

DB_FOLDER = "data"
DB_NAME = "offers.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

def init_db():
    """Initializes the SQLite database and creates the offers table."""
    # Ensure the data directory exists
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create table with specified schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                customer_name TEXT,
                catalog TEXT,
                products_json TEXT,
                total_price REAL,
                discount REAL,
                duration TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()