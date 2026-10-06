import os
import sqlite3
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "heart_disease.db")

def get_db_connection(use_mysql=False, mysql_config=None):
    """
    Returns a database connection. Defaults to SQLite for self-contained zero-config execution.
    Falls back to SQLite if MySQL connection fails.
    """
    if use_mysql and MYSQL_AVAILABLE and mysql_config:
        try:
            conn = mysql.connector.connect(**mysql_config)
            return conn, "mysql"
        except Exception as e:
            print(f"[Database Warning] MySQL connection failed ({e}). Falling back to SQLite.")

    # SQLite Fallback / Default
    conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"

def init_db(use_mysql=False, mysql_config=None):
    """
    Initializes user tables, medical record tables, and default seed data.
    """
    conn, db_type = get_db_connection(use_mysql, mysql_config)
    cursor = conn.cursor()

    if db_type == "sqlite":
        # Create Tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT DEFAULT 'doctor',
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT DEFAULT 'patient',
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Insert Seed Data if missing
        cursor.execute("SELECT COUNT(*) FROM doctor WHERE email='sahilkhade@gmail.com'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO doctor (type, name, email, password) VALUES ('doctor', 'Dr. Sahil Khade', 'sahilkhade@gmail.com', 'sahil')")

        cursor.execute("SELECT COUNT(*) FROM patient WHERE email='sahil@gmail.com'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO patient (type, name, email, password) VALUES ('patient', 'Sahil Patient', 'sahil@gmail.com', '123')")

        conn.commit()
        conn.close()
        print(f"[Database Init] SQLite database initialized successfully at: {SQLITE_DB_PATH}")

    else:
        # MySQL tables setup
        cursor.execute("CREATE TABLE IF NOT EXISTS doctor (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(20), name VARCHAR(50), email VARCHAR(100) UNIQUE, password VARCHAR(50));")
        cursor.execute("CREATE TABLE IF NOT EXISTS patient (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(20), name VARCHAR(50), email VARCHAR(100) UNIQUE, password VARCHAR(50));")
        cursor.execute("CREATE TABLE IF NOT EXISTS assessment_history (id INT AUTO_INCREMENT PRIMARY KEY, user_email VARCHAR(100), assessment_type VARCHAR(50), prediction VARCHAR(100), confidence FLOAT, details TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);")
        
        try:
            cursor.execute("INSERT IGNORE INTO doctor (type, name, email, password) VALUES ('doctor', 'Dr. Sahil Khade', 'sahilkhade@gmail.com', 'sahil')")
            cursor.execute("INSERT IGNORE INTO patient (type, name, email, password) VALUES ('patient', 'Sahil Patient', 'sahil@gmail.com', '123')")
            conn.commit()
        except Exception:
            pass
        cursor.close()
        conn.close()
        print("[Database Init] MySQL database initialized successfully.")

if __name__ == "__main__":
    init_db()
