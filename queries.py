import sqlite3

connection = sqlite3.connect("HDMessengerDB.db")
c = connection.cursor()
        
c.execute("""
        INSERT INTO Users
        VALUES('admin', 'admin', 1)
        """)
connection.commit()
c.execute("SELECT * FROM Users")
print(c.fetchall())