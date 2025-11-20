# src/test_db.py
import db_connection

conn = db_connection.connect_db()
if conn:
    print("✅ Connected to MySQL database!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    print("Users in DB:", rows)
    conn.close()
else:
    print("❌ Failed to connect.")
