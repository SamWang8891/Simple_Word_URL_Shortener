import os
import sqlite3


def load_dictionary(dbfile, conn, cur, txtfile):
    cur.execute('DROP TABLE IF EXISTS dict')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS dict (
        word TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    )
    ''')
    
    with open(txtfile, 'r') as file:
        words = file.readlines()
    
    for word in words:
        w = word.strip()
        cur.execute('''
        INSERT INTO dict (word) VALUES (?)
        ''', (w,))
    
    conn.commit()


def make_urls(dbfile, conn, cur):
    cur.execute('DROP TABLE IF EXISTS urls')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        orig TEXT,
        short TEXT
    )
    ''')
    
    conn.commit()


def make_login(dbfile, conn, cur):
    cur.execute('DROP TABLE IF EXISTS login')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS login (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    ''')
    
    conn.commit()
    
    # default username: admin, password: password
    username = "admin"
    password = "$argon2id$v=19$m=102400,t=2,p=8$l7bMrtz82jfIJk5Uq82mGQ$1ABNbzjrDJ6WPNnhGi5UpQ"
    cur.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
    
    conn.commit()
    
    

if __name__ == '__main__':
    txtfile = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
    dbfile = os.path.join(os.path.dirname(__file__), 'docker/db/data.db')
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    load_dictionary(dbfile, conn, cur, txtfile)
    make_urls(dbfile, conn, cur)
    make_login(dbfile, conn, cur)
    conn.close()