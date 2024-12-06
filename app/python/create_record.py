import sqlite3
import os
import re
import segno
from dotenv import load_dotenv



if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    base_url = os.getenv('BASE_URL')
    dbfile = os.path.join(os.path.dirname(__file__), 'data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    original_url = input()

    if not original_url.startswith(('https://', 'http://')):
        original_url = 'https://' + original_url

    
    cur.execute("SELECT word FROM dict WHERE used = 0 LIMIT 1")
    shortened_url = cur.fetchone()[0]
    cur.execute("UPDATE dict SET used = 1 WHERE word = ?", (shortened_url,))

    cur.execute("SELECT orig FROM urls WHERE orig = ?", (original_url,))
    if not cur.fetchone():
        cur.execute("INSERT INTO urls (orig, short) VALUES (?, ?)", (original_url, shortened_url))
        print(f"{base_url}/{shortened_url}")
    else: 
        cur.execute("SELECT short FROM urls WHERE orig = ?", (original_url,))
        existing_short = cur.fetchone()[0]
        cur.execute("UPDATE dict SET used = 0 WHERE word = ?", (existing_short,))
        cur.execute("UPDATE urls SET short = ? WHERE orig = ?", (shortened_url, original_url))
        print(f"{base_url}/{shortened_url}")

    
    url = base_url + "/" + shortened_url
    qrcode = segno.make_qr(url)
    filename = re.sub(r'[^a-zA-Z0-9]', '.', url)
    qrcode.save(f"/app/images/{filename}.png")

    con.commit()
    con.close()
