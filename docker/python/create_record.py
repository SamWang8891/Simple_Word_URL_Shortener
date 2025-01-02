import sqlite3
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '/docker/.env'))
    base_url = os.getenv('BASE_URL')
    dbfile = os.path.join(os.path.dirname(__file__), '/docker/db/data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    
    original_url = input()
    original_url = original_url.strip("'")
    original_url = original_url.decode('base64')
    
    if not original_url.startswith(('https://', 'http://')):
        original_url = 'https://' + original_url

    cur.execute("SELECT word FROM dict WHERE used = 0 ORDER BY RANDOM() LIMIT 1")
    shortened_url = cur.fetchone()[0]
    cur.execute("UPDATE dict SET used = 1 WHERE word = ?", (shortened_url,))

    cur.execute("SELECT orig FROM urls WHERE orig = ?", (original_url,))
    if cur.fetchone():
        cur.execute("SELECT short FROM urls WHERE orig = ?", (original_url,))
        existing_short = cur.fetchone()[0]
        cur.execute("UPDATE dict SET used = 0 WHERE word = ?", (existing_short,))
        cur.execute("UPDATE urls SET short = ? WHERE orig = ?", (shortened_url, original_url))
        print(f"{base_url}/{shortened_url}")
    else: 
        cur.execute("INSERT INTO urls (orig, short) VALUES (?, ?)", (original_url, shortened_url))
        print(f"{base_url}/{shortened_url}")
        

    con.commit()
    con.close()