import sqlite3
import json

conn = sqlite3.connect('games.sqlite')
cursor = conn.cursor()

array_data = [1, 2, 3, 4, 5]
json_data = json.dumps(array_data)

cursor.execute("INSERT INTO games (data) VALUES (?)", (json_data,))
conn.commit()

conn.close()
