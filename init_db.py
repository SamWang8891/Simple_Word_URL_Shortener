import os
import sqlite3


def load_dictionary(dbfile, conn, cursor, txtfile):
    cursor.execute('DROP TABLE IF EXISTS dict')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dict (
        word TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    )
    ''')
    
    with open(txtfile, 'r') as file:
        words = file.readlines()
    
    for word in words:
        w = word.strip()
        cursor.execute('''
        INSERT INTO dict (word) VALUES (?)
        ''', (w,))
    
    conn.commit()


def make_urls(dbfile, conn, cursor):
    cursor.execute('DROP TABLE IF EXISTS urls')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        orig TEXT,
        short TEXT
    )
    ''')
    
    conn.commit()




if __name__ == '__main__':
    txtfile = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
    dbfile = os.path.join(os.path.dirname(__file__), 'app/python/data.db')
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    load_dictionary(dbfile, conn, cursor, txtfile)
    make_urls(dbfile, conn, cursor)
    conn.close()