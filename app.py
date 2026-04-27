from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from functools import wraps
import sqlite3
import os
import csv
import io

app = Flask(__name__)

# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'mmsu_medical_dashboard_secret_2024_CHANGE_IN_PRODUCTION')

# Configure session for better security
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

DB_PATH = "mmsu.db"

# Admin credentials - Use environment variables in production
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'mmsu2024')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            blood TEXT,
            department TEXT,
            conditions TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    return send_from_directory('.', 'login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/')
@login_required
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM personnel")

    count = 0
    for row in reader:
        c.execute("INSERT INTO personnel (name, gender, blood, department, conditions) VALUES (?, ?, ?, ?, ?)", (
            row.get('name', ''),
            row.get('gender', ''),
            row.get('blood', ''),
            row.get('department', ''),
            row.get('conditions', '')
        ))
        count += 1

    conn.commit()
    conn.close()
    return jsonify({'message': f'{count} records uploaded successfully!'})

@app.route('/personnel', methods=['GET'])
@login_required
def get_personnel():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, gender, blood, department, conditions FROM personnel")
    rows = c.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'name': row[0],
            'gender': row[1],
            'blood': row[2],
            'department': row[3],
            'conditions': row[4].split('|') if row[4] else []
        })
    return jsonify(data)

@app.route('/personnel/add', methods=['POST'])
@login_required
def add_personnel():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO personnel (name, gender, blood, department, conditions) VALUES (?, ?, ?, ?, ?)", (
        data.get('name', ''),
        data.get('gender', ''),
        data.get('blood', ''),
        data.get('department', ''),
        '|'.join(data.get('conditions', []))
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Personnel added successfully!'})

@app.route('/personnel/delete/<int:pid>', methods=['DELETE'])
@login_required
def delete_personnel(pid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM personnel WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted successfully!'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f"✅ MMSU Medical Dashboard running at http://127.0.0.1:{port}")
    print(f"⚠️  Default credentials - Username: {ADMIN_USERNAME}, Password: {ADMIN_PASSWORD}")
    print("⚠️  IMPORTANT: Change credentials before deploying to production!")
    app.run(host='0.0.0.0', port=port, debug=debug)
