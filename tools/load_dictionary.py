import os
import sqlite3


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/app/python/data.db')
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS dict')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dict (
        word TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    )
    ''')
    
    txtfile = os.path.join(os.path.dirname(__file__), '/app/python/tools/words.txt')
    with open(txtfile, 'r') as file:
        words = file.readlines()
    
    for word in words:
        w = word.strip()
        cursor.execute('''
        INSERT INTO dict (word) VALUES (?)
        ''', (w,))
    
    conn.commit()
    conn.close()