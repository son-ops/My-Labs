from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
from urllib.parse import unquote
import re
import string
import random

app = Flask(__name__)

FLAG = 'SSS{' + "".join(random.choices(string.digits+string.ascii_letters, k=5)) + '-flag}'

def con():
    if not os.path.exists(os.getenv("SQLITE_DB_PATH")):
        con = sqlite3.connect(os.getenv("SQLITE_DB_PATH"))
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS menu (id integer primary key, name text, price integer)")
        cur.execute("INSERT INTO menu VALUES (1, 'Pizza', 5555), (2, 'Bread', 6666), (3, 'Noodles', 3333)")
        cur.execute("CREATE TABLE IF NOT EXISTS flag (flag text)")
        cur.execute("INSERT INTO flag VALUES (?)", (FLAG,))
        con.commit()
    else:
        con = sqlite3.connect(os.getenv("SQLITE_DB_PATH"))
    return con

@app.route("/")
def index():
    return redirect(url_for("search"))

@app.route("/search")
def search():
    by = request.args.get("by")
    if by is not None:
        if re.findall(r"[^\d%]", by):
            return {"status": "by param only accept character in [0-9%]"}
        by = unquote(unquote(by))
    conn = con()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM menu")
        data = cur.fetchall()
        if by:
            cur.execute(f"SELECT * FROM menu ORDER BY {by}")
            data = cur.fetchall()
    except:
        pass
    conn.close()
    return render_template("search.html", by=by, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))
