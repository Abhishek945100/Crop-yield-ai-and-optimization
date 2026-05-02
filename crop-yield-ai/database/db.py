import sqlite3

def create_tables():
    conn = sqlite3.connect("crop_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_name TEXT,
        crop TEXT,
        predicted_yield REAL,
        estimated_profit REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_record(data):
    conn = sqlite3.connect("crop_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO historical_records
    (farmer_name, crop, predicted_yield, estimated_profit)
    VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect("crop_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM historical_records")
    rows = cursor.fetchall()
    conn.close()
    return rows