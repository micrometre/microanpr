import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash




conn = sqlite3.connect('./instance/flaskralpr.sqlite')
c = conn.cursor()
id = 1
username = ("test")
password = ("test")
c.execute("INSERT INTO user (username, password) VALUES (?, ?)",(username, generate_password_hash(password)),)
c.execute("INSERT INTO user (username, password) VALUES (?, ?)",(username, generate_password_hash(password)),)
conn.commit()
print("Password added.")
