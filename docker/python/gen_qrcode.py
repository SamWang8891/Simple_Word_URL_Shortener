import segno
import os
from dotenv import load_dotenv
import re

def add_prot(url):
    if not url.startswith(('https://', 'http://')):
        url = 'https://' + url
    return url


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '/docker/.env'))
    base_url = os.getenv('BASE_URL')
    
    url = input()
    url = url.strip("'")
    url = url.decode("base64")
    
    url = add_prot(url)
    
    qrcode = segno.make_qr(url)
    filename = re.sub(r'[^a-zA-Z0-9]', '.', url)
    qrcode.save(f"/docker/web/images/{filename}.png")
    print(f"{base_url}/images/{filename}.png")