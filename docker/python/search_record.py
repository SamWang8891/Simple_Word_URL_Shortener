import sqlite3
import os


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/docker/db/data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    
    search_url = input()
    search_url = search_url.strip("'")
    search_url = search_url.decode('base64')
    
    cur.execute("SELECT orig FROM urls WHERE short = ?", (search_url,))
    result = cur.fetchone()
    if not result:
        print("404.html")
    else:
        shortened_url = result[0]
        print(shortened_url)
    
    con.close()
