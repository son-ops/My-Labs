import os
import subprocess
from flask import Flask, render_template, request

HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", "5000"))
TIMEOUT = os.getenv("FETCH_TIMEOUT", "3")
LIMIT = int(os.getenv("MAX_RESPONSE_BYTES", "16384"))

app = Flask(__name__)

def fetch(url):
    proc = subprocess.run(
        ["curl", "-sS", "--max-time", TIMEOUT, "-o", "-", url],
        capture_output=True,
        check=False,
    )
    body = proc.stdout[:LIMIT]
    err = proc.stderr.decode(errors="replace").strip()
    if proc.returncode and not body:
        raise RuntimeError(err or f"curl exited with status {proc.returncode}")
    return {
        "fetcher": "curl",
        "bytes": len(body),
        "body": body.decode("utf-8", errors="replace"),
        "warning": err if proc.returncode else "",
    }

@app.route("/")
def index():
    url = request.args.get("url", "").strip()
    result, error = None, None
    if url:
        try:
            result = fetch(url)
        except Exception as exc:
            error = str(exc)
    return render_template("index.html", target=url, result=result, error=error)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
