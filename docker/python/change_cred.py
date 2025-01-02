from argon2 import PasswordHasher
import sqlite3
import os


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/docker/db/data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    
    old_username = input()
    new_username = input()
    new_password = input()
    
    old_username = old_username.strip("'")
    new_username = new_username.strip("'")
    new_password = new_password.strip("'")
    old_username = old_username.decode('base64')
    new_username = new_username.decode('base64')
    new_password = new_password.decode('base64')
    
    ph = PasswordHasher()
    password = ph.hash(new_password)
    
    cur.execute("SELECT password FROM login WHERE username = ?", (old_username,))
    result = cur.fetchone()
    if not result:
        print("0")
    else:
        cur.execute("UPDATE login SET username = ? WHERE username = ?", (new_username, old_username))    
        cur.execute("UPDATE login SET password = ? WHERE username = ?", (new_password, new_username))
        con.commit()
        print("1")
    
    con.close()
    
    
        
    