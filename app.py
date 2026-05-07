from flask import Flask, request, redirect, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# Create DB automatically
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.close()

init_db()

def get_db():
    return sqlite3.connect("users.db")

# Templates (inside same file)
login_page = """
<h2>Login</h2>
<form method="post">
<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>
<button type="submit">Login</button>
</form>
<a href="/register">Register</a>
"""

register_page = """
<h2>Register</h2>
<form method="post">
<input name="username" placeholder="Username"><br>
<input name="password" type="password" placeholder="Password"><br>
<button type="submit">Register</button>
</form>
<a href="/login">Login</a>
"""

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = get_db()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template_string(register_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        conn.close()

        if user:
            session['user'] = u
            return redirect('/dashboard')
        else:
            return "Invalid login"

    return render_template_string(login_page)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"<h2>Welcome {session['user']}</h2><a href='/logout'>Logout</a>"
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)# User Login and Registration System

