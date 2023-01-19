import sqlite3

conn = sqlite3.connect("poe-reboot.db")

c = conn.cursor()

c.execute("select * from device")

print(c.fetchall())

conn.commit()

conn.close();