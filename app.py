from flask import Flask, render_template, request, redirect, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secureprojectkey"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT,
        uploaded_by TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",
                    (username, password, 'user'))

        conn.commit()
        conn.close()

        flash('Registration Successful')
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]

            if user[3] == 'admin':
                return redirect('/admin')

            return redirect('/dashboard')

        flash('Invalid Credentials')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO resources(title,filename,uploaded_by) VALUES(?,?,?)",
                (title, filename, session['username'])
            )

            conn.commit()
            conn.close()

            flash('Resource Uploaded Successfully')
        else:
            flash('Invalid file type. Only PDF, DOC, DOCX, TXT, PPT, and PPTX files are allowed.')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM resources")
    resources = cur.fetchall()

    conn.close()

    return render_template('dashboard.html', resources=resources)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin')
def admin():

    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM resources")
    resources = cur.fetchall()

    conn.close()

    return render_template('admin.html', users=users, resources=resources)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
@app.after_request
def add_security_headers(response):

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Cache-Control'] = 'no-store'

    return response
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)