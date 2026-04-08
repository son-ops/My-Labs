from flask import Flask, request, render_template, send_file
from pathlib import Path
import unicodedata
from time import sleep

app = Flask(__name__)

def norm(input):
    return unicodedata.normalize('NFKC',input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resource')
def resource():
    image = request.args.get("image")
    if not image:
        return render_template('resource.html')
    if Path(image).is_absolute() or '..' in image:
        return {"status": "travesal detect"}
    path = Path('resources') / norm(image)
    if 'flag' in str(path):
        return {"status": "Can't read flag directly"}
    if Path(path).is_file():
        return send_file(path)
    return {"status": "Read file error"}

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    file = request.files.get('file')
    with open(file.filename, 'ab') as f:
        sleep(4)
        return {"status": "Only admin can upload file"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)