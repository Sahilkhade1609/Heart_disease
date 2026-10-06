import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham@072007",
        database="heart"
    )
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS doctor (type VARCHAR(20), name VARCHAR(50), email VARCHAR(100), password VARCHAR(50));")
    cursor.execute("CREATE TABLE IF NOT EXISTS patient (type VARCHAR(20), name VARCHAR(50), email VARCHAR(100), password VARCHAR(50));")
    cursor.execute("INSERT INTO doctor VALUES ('doctor','sahil','sahilkhade@gmail.com','sahil');")
    cursor.execute("INSERT INTO patient VALUES ('patient','sahil','sahil@gmail.com','123');")
    db.commit()
    cursor.close()
    print("Tables created and populated successfully.")
except Exception as e:
    print("Error:", e)
