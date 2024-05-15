import hashlib
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash






conn = sqlite3.connect('./instance/flaskralpr.sqlite')
c = conn.cursor()
id = 1
username = ("username: test")
password = ("password: test")
#default_pass = generate_password_hash(txtPassword)
#c.execute("insert into user values (?, ?)", ( currentUser, default_pass))
c.execute("INSERT INTO user (username, password) VALUES (?, ?)",(username, generate_password_hash(password)),)
