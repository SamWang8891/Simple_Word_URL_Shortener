import os
import sqlite3 #built-in module, no need to pip install


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/app/python/data.db')
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS urls')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        orig TEXT,
        short TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

