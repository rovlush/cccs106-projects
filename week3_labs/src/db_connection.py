import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",      # 👈 leave blank if phpMyAdmin root has no password
            database="fletapp"
        )
        return conn
    except mysql.connector.Error as e:
        print("❌ Database connection failed:", e)
        return None

