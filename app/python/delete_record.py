import sqlite3
from dotenv import load_dotenv
import os


def search(cur, url, search_target):
    cur.execute(f"SELECT short FROM urls WHERE {search_target} = ?", (url,))
    return cur.fetchone()


def delete(con, cur, url, search_target, result):
    search_text = result[0]
    cur.execute(f"DELETE FROM urls WHERE {search_target} = ?", (url,))
    cur.execute("UPDATE dict SET used = 0 WHERE word = ?", (search_text,))
    print("Record deleted.")
    con.commit()



if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    base_url = os.getenv('BASE_URL')
    base_url_without_protocol = base_url.split('://')[1]
    dbfile = os.path.join(os.path.dirname(__file__), 'data.db')
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    input_url = input("").rstrip('/')

    # Complete URL
    result = search(cur, input_url, 'orig')
    if result:
        delete(con, cur, input_url, 'orig', result)
        exit()

    # Missing http://
    if not input_url.startswith('http://'):
        mod_url = 'http://' + input_url
        result = search(cur, mod_url, 'orig')
        if result:
            delete(con, cur, mod_url, 'orig', result)
            exit()
    
    # Missing https://
    if not input_url.startswith('https://'): 
        mod_url = 'https://' + input_url
        result = search(cur, mod_url, 'orig')
        if result:
            delete(con, cur, mod_url, 'orig', result)
            exit()

    # only the shorted generated part
    result = search(cur, input_url, 'short')
    if result:
        delete(con, cur, input_url, 'short', result)
        exit()
    else:
        if input_url.startswith(base_url): # the shortened part plus the base url with protocol
            mod_url = input_url[len(base_url):].lstrip('/')
            result = search(cur, mod_url, 'short')
            if result:
                delete(con, cur, mod_url, 'short', result)
                exit()
        elif input_url.startswith(base_url_without_protocol): # the shortened part plus the base url without protocol
            mod_url = input_url[len(base_url_without_protocol):].lstrip('/')
            result = search(cur, mod_url, 'short')
            if result:
                delete(con, cur, mod_url, 'short', result)
                exit()
        else:
            print("Record not found.")
            exit()

    con.close()
