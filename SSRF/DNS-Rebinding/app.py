import ipaddress
import socket, time
from urllib.parse import urlparse
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
REBIND_DELAY_SECONDS = 1

def is_internal_ip(ip_address):
    ip = ipaddress.ip_address(ip_address)
    return (
        ip.is_loopback
        or ip.is_private
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
        or ip.is_reserved
    )

def validate(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https') or not parsed_url.hostname:
        return False, 'Invalid URL', None
    if parsed_url.username or parsed_url.password:
        return False, 'URL userinfo is not allowed', None
    try:
        parsed_url.port
    except ValueError:
        return False, 'Invalid port', None
    try:
        ip_address = socket.gethostbyname(parsed_url.hostname)
    except socket.gaierror:
        return False, 'Cannot resolve hostname', None
    if is_internal_ip(ip_address):
        return False, f'SSRF detected: {ip_address}', ip_address
    return True, f'Validation passed: {parsed_url.hostname} -> {ip_address}', ip_address

@app.route('/')
def index():
    url = request.args.get('url', '').strip()
    if not url:
        return render_template('index.html')
    allowed, message, validation_ip = validate(url)
    if not allowed:
        return render_template(
            'index.html',
            message=message,
            validation_ip=validation_ip
        )
    try:
        session = requests.Session()
        session.trust_env = False
        time.sleep(REBIND_DELAY_SECONDS)
        response = session.get(url, timeout=3)
    except requests.RequestException as error:
        return render_template(
            'index.html',
            message=message,
            validation_ip=validation_ip,
            error=str(error)
        ), 502

    return render_template(
        'index.html',
        message=message,
        validation_ip=validation_ip,
        status_code=response.status_code,
        response=response.text
    )

@app.route('/flag')
def flag():
    if request.remote_addr == '127.0.0.1':
        return {"FLAG": r"SSS{flaggggggggggg}"}
    return {"status": "Forbidden"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
