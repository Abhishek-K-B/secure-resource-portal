from flask import Flask, render_template, request, redirect, session, flash, send_from_directory
from markupsafe import escape
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)
app.secret_key = "secureprojectkey"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        subject TEXT,
        description TEXT,
        filename TEXT,
        uploaded_by TEXT,
        upload_date TEXT
    )
    ''')

    cur.execute("SELECT * FROM users WHERE username='admin'")
    admin = cur.fetchone()

    if not admin:
        admin_password = generate_password_hash('admin123')
        cur.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            ('admin', admin_password, 'admin')
        )

    conn.commit()
    conn.close()


init_db()


@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
def home():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        password = generate_password_hash(request.form['password'])

        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(username,password,role) VALUES(?,?,?)",
                (username, password, 'user')
            )
            conn.commit()
            conn.close()

            flash('Registration successful. Please login.')
            return redirect('/login')

        except sqlite3.IntegrityError:
            flash('Username already exists.')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def login():
    if request.method == 'POST':
        username = escape(request.form['username'].strip())
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (str(username),))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]

            if user[3] == 'admin':
                return redirect('/admin')

            return redirect('/dashboard')

        print(f"Failed login attempt for user: {username}")
        flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = escape(request.form['title'])
        subject = escape(request.form['subject'])
        description = escape(request.form['description'])
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            upload_date = datetime.now().strftime("%d-%m-%Y %H:%M")

            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO resources(title,subject,description,filename,uploaded_by,upload_date) VALUES(?,?,?,?,?,?)",
                (str(title), str(subject), str(description), filename, session['username'], upload_date)
            )
            conn.commit()
            conn.close()

            flash('Resource uploaded successfully.')
        else:
            flash('Invalid file type. Only PDF, DOC, DOCX, TXT, PPT, and PPTX files are allowed.')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources ORDER BY id DESC")
    resources = cur.fetchall()
    conn.close()

    return render_template('dashboard.html', resources=resources)


@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM resources ORDER BY id DESC")
    resources = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM resources")
    total_resources = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    total_admins = cur.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        users=users,
        resources=resources,
        total_users=total_users,
        total_resources=total_resources,
        total_admins=total_admins
    )


@app.route('/delete_resource/<int:resource_id>')
def delete_resource(resource_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM resources WHERE id=?", (resource_id,))
    conn.commit()
    conn.close()

    flash('Resource deleted successfully.')
    return redirect('/admin')


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=? AND role!='admin'", (user_id,))
    conn.commit()
    conn.close()

    flash('User deleted successfully.')
    return redirect('/admin')


@app.route('/download/<filename>')
def download(filename):
    if 'username' not in session:
        return redirect('/login')

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

