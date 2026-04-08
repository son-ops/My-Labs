from flask import Flask, request, render_template, send_file
from utils import writer
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    path = request.args.get("file")
    if not path:
        return render_template('list.html', files=os.listdir(os.getenv("BASE")))
    try:
        path = Path(os.getenv("BASE")) / Path(path).name
        return send_file(path)
    except:
        return {"status": "File not found or error"}
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    f = request.files['file']
    data = f.read()
    path = f.filename
    try:
        if writer(path,data):
            return {"status": "Upload successfully"}
    except Exception as e:
        return {"status": "Upload error"}
    
@app.route('/health')
def restart():
    out = __import__("health").check()
    return {"info": out}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
