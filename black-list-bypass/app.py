from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import re
import random
import os
import string

app = Flask(__name__)

FLAG = 'SSS{' + ''.join(random.choices(string.digits + string.ascii_letters, k=10)) + '-flag}'
def con_db():
    conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    port=int(os.getenv('DB_PORT')),
    passwd=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_NAME'),
    charset="utf8mb4"
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY AUTO_INCREMENT,username VARCHAR(255),password VARCHAR(255))")
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "123"))
    cur.execute("CREATE TABLE IF NOT EXISTS flag (flag VARCHAR(255))")
    cur.execute("INSERT INTO flag VALUES (%s)", (FLAG,))
    return conn

FORBIDEN = r"\s|union|select|and|or|\|\||\&\&|'|\"|/|\*|-|#|case|when|sleep|benchmark"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    query = f"SELECT * FROM users WHERE username='{username}' and password='{password}'"
    if re.findall(FORBIDEN, username, re.I | re.S) or re.findall(FORBIDEN, password, re.I | re.S):
        return {"status": "False"}
    clean_query = "".join(c for c in query if c.isascii())
    con = con_db()
    cur = con.cursor()
    try: 
        cur.execute(clean_query)
        user = cur.fetchone()
        con.close()
        if user:
            return {"status": "Login successfully"}
    except:
        return {"status":"False"}
    return {"status": "False"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))
    