import sqlite3
import os

def initialize_database(db_path="database.db"):
    # Check if the database file exists and is empty
    if not os.path.exists(db_path):
        print("Database file does not exist, creating new database.")
    else:
        # Check if the database is empty
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
        table_count = cursor.fetchone()[0]
        
        if table_count == 0:
            print("Database is empty. Creating tables and adding default data.")
        else:
            print("Database exists, checking tables.")
            cursor.execute("SELECT COUNT(*) FROM toppings")
            
            if cursor.fetchone()[0] > 0:
                print("Toppings table is not empty.")
            else:
                print("Toppings table is empty.")
                
            cursor.execute("SELECT COUNT(*) FROM pizzas")
            if cursor.fetchone()[0] > 0:
                print("Pizzas table is not empty.")
            else:
                print("Pizzas table is empty.")
            conn.close()

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the toppings table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS toppings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Create the pizzas table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pizzas (
            name TEXT PRIMARY KEY, -- Pizza name is the unique ID
            topping1 TEXT NOT NULL,
            topping2 TEXT,
            topping3 TEXT,
            UNIQUE (topping1, topping2, topping3)
        )
    """)

    # Insert default toppings if the toppings table is empty
    cursor.execute("SELECT COUNT(*) FROM toppings")
    if cursor.fetchone()[0] == 0:
        toppings = [
            ("Cheese",),
            ("Pepperoni",),
            ("Mushrooms",)
        ]
        cursor.executemany("INSERT INTO toppings (name) VALUES (?)", toppings)
        print("Inserted default toppings.")

    # Insert default pizzas if the pizzas table is empty
    cursor.execute("SELECT COUNT(*) FROM pizzas")
    if cursor.fetchone()[0] == 0:
        pizzas = [
            ("Classic Cheese", "Cheese", None, None),
            ("Pepperoni Lover", "Cheese", "Pepperoni", None),
            ("Veggie Delight", "Cheese", "Mushrooms", None)
        ]
        cursor.executemany("""
            INSERT INTO pizzas (name, topping1, topping2, topping3)
            VALUES (?, ?, ?, ?)
        """, pizzas)
        print("Inserted default pizzas.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
