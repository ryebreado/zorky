import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO gamestate (username, content) VALUES (?, ?)",
            ('Samuel Jr. The First', 'Cucumber')
            )

connection.commit()
connection.close()