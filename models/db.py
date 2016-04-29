import sqlite3
conn = sqlite3.connect('GeoNews.db')

c = conn.cursor()

c.execute('''CREATE TABLE locations ( name text, gmap_json text )''')

conn.commit()

conn.close()
