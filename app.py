from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, user TEXT, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'username' in session:
        conn = sqlite3.connect('database.db')
        posts = conn.execute("SELECT * FROM posts").fetchall()
        conn.close()
        return render_template('index.html', posts=posts, username=session['username'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd)).fetchone()
        conn.close()
        if user:
            session['username'] = uname
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        content = request.form['content']
        user = session['username']
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO posts (user, content) VALUES (?, ?)", (user, content))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('post.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
