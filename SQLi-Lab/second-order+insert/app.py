from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import string
import random
import os
import time

FLAG = 'SSS{' + ''.join(random.choices(string.digits + string.ascii_letters, k=10)) + '-flag}'
app = Flask(__name__)
app.secret_key = "---secret---"

def con_db():
    con = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    charset="utf8mb4"
    )
    return con

def init_db():
    con = con_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255),password VARCHAR(255))")
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "123"))
    cur.execute("CREATE TABLE IF NOT EXISTS flag (flag VARCHAR(255))")
    cur.execute("INSERT INTO flag VALUES (%s)", (FLAG,))
    cur.execute("CREATE TABLE IF NOT EXISTS books (name text, content text, author text)")
    con.commit()
    con.close()

@app.route("/")
def index():
    if "username" in session:
        return render_template('index.html', name=session.get('username'))
    return redirect(url_for('login'))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    username = request.form.get("username")
    password = request.form.get("password")
    con = con_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users where username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    con.close()
    if user:
        session['username'] = user[0]
        return redirect(url_for('index'))
    return render_template('login.html', message="Invalid username or password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    con = con_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users where username = %s", (username,))
    user = cur.fetchone()
    if user:
        con.close()
        return render_template("register.html", message="Username already exists")
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    con.commit()
    con.close()
    return redirect(url_for('login'))

@app.route("/my-book", methods = ["GET", "POST"])
def my_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    con = con_db()
    cur = con.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM books where author = %s", (session['username'],))
        posts = cur.fetchall()
        return render_template("book.html", post=posts, name=session['username'])
    book_name = request.form.get("book_name")
    content = request.form.get("content")
    try:
        cur.execute(f"INSERT INTO books VALUES (%s, %s, '{session['username']}')", (book_name, content))
    except Exception as e:
        return {"error": str(e)}
    con.commit()
    con.close()
    return redirect(url_for('my_book'))

if __name__ == "__main__":
    time.sleep(15)
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))


