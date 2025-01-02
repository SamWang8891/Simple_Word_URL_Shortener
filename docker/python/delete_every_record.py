import sqlite3
import os


if __name__ == '__main__':
    dbfile = os.path.join(os.path.dirname(__file__), '/docker/db/data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    cur.execute("DELETE FROM urls")
    con.commit()

    cur.execute("UPDATE dict SET used = 0;")
    con.commit()
    
    print("Purged every record.")
    
    con.close()
