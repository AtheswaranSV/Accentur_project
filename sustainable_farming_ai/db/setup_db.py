import sqlite3

conn = sqlite3.connect("farming.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        soil_type INTEGER,
        rainfall REAL,
        temperature REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER,
        recommendation TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()
print("Database initialized!")
