from flask import Flask, request, render_template_string, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Insecure Secret Key

# Initialize SQLite database
conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, secret TEXT)''')
c.execute("INSERT INTO users (username, password, secret) VALUES ('admin', 'admin_pass', 'Admin Secret Message')")
c.execute("INSERT INTO users (username, password, secret) VALUES ('user', 'user_pass', 'User Secret Message')")
conn.commit()

@app.route('/')
def index():
    return "Welcome to the Vulnerable App!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        
        if user:
            session['username'] = username
            return render_template_string(f"<h2>Welcome, {username}!</h2><a href='/secret'>Go to Secret Page</a>")
        else:
            error = "Invalid credentials!"
    
    
    return '''
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    ''' + (f'<p style="color: red;">{error}</p>' if error else '')

@app.route('/secret')
def secret():
    username = session.get('username')
    if username:
        c.execute(f"SELECT secret FROM users WHERE username = '{username}'")
        secret = c.fetchone()[0]
        return render_template_string(f"<h2>{username}'s Secret Message: {secret}</h2>")
    else:
        return "You must be logged in to view the secret message!", 403

if __name__ == '__main__':
    app.run(debug=True)
