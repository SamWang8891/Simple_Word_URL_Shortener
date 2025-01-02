from argon2 import PasswordHasher
import sqlite3
import os
import base64


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/docker/db/data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    
    username = input()
    password = input()
    
    username = username.strip("'")
    password = password.strip("'")
    username = base64.b64decode(username).decode('utf-8')
    password = base64.b64decode(password).decode('utf-8')
    
    cur.execute("SELECT password FROM login WHERE username = ?", (username,))
    result = cur.fetchone()
    if not result:
        print("0")
    else:
        stored_password = result[0]
        ph = PasswordHasher()
        print(f"The username is {username} and the password is {password}")
        try:
            ph.verify(stored_password, password)
            print("1")
        except:
            print("0")
    
    # print(f"The username is {username} and the password is {password}")