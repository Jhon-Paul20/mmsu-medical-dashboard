from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
import os
import csv
import io
import secrets
import psycopg2
import psycopg2.extras

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR)

app.secret_key = os.environ.get('SECRET_KEY', 'mmsu_medical_dashboard_secret_2024_CHANGE_IN_PRODUCTION')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'mmsu2024')

# ── DATABASE ──────────────────────────────────────────────────────────────────

def get_db():
    """Open a new PostgreSQL connection using DATABASE_URL from environment."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL environment variable is not set.')
    # Railway sometimes provides postgres:// — psycopg2 needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return psycopg2.connect(database_url)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS personnel (
            id   SERIAL PRIMARY KEY,
            name TEXT,
            gender TEXT,
            blood TEXT,
            department TEXT,
            conditions TEXT
        )
    ''')
    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM personnel')
    count = c.fetchone()[0]
    if count == 0:
        records = [
            ('Ana Reyes',         'Female', 'O+',  'CHS',  'Hypertension|Diabetes'),
            ('Juan dela Cruz',    'Male',   'A+',  'COE',  'Asthma'),
            ('Maria Santos',      'Female', 'B+',  'CTE',  'Allergies|Migraine'),
            ('Carlos Mendoza',    'Male',   'AB+', 'CBEA', 'Hypertension'),
            ('Liza Fernandez',    'Female', 'O-',  'CAS',  'Anemia'),
            ('Ramon Torres',      'Male',   'A+',  'CHS',  'Diabetes|Obesity'),
            ('Gloria Villanueva', 'Female', 'B-',  'COE',  'Arthritis'),
            ('Eduardo Garcia',    'Male',   'O+',  'CTE',  'Heart Disease'),
            ('Nora Bautista',     'Female', 'A-',  'CBEA', 'Thyroid Disorder|Hypertension'),
            ('Miguel Ramos',      'Male',   'AB-', 'CAS',  'Gastritis'),
            ('Josie Aquino',      'Female', 'O+',  'CHS',  'Asthma|Allergies'),
            ('Andres Flores',     'Male',   'B+',  'COE',  'Ulcer'),
            ('Cristina Lopez',    'Female', 'A+',  'CTE',  'Mental Health'),
            ('Roberto Cruz',      'Male',   'O-',  'CBEA', 'Hypertension|Kidney Disease'),
            ('Teresita Ocampo',   'Female', 'B+',  'CAS',  'Diabetes'),
            ('Danilo Castillo',   'Male',   'A+',  'CHS',  'Bronchitis'),
            ('Maribel Reyes',     'Female', 'AB+', 'COE',  'Migraine|Anemia'),
            ('Ernesto Salazar',   'Male',   'O+',  'CTE',  'Liver Disease'),
            ('Rowena Pascual',    'Female', 'A-',  'CBEA', 'Asthma'),
            ('Felix Navarro',     'Male',   'B-',  'CAS',  'Heart Disease|Diabetes'),
        ]
        psycopg2.extras.execute_batch(
            c,
            'INSERT INTO personnel (name, gender, blood, department, conditions) VALUES (%s, %s, %s, %s, %s)',
            records
        )
        conn.commit()
        print(f'Seeded {len(records)} personnel records.')
    conn.close()

init_db()
seed_db()

# ── AUTH / CSRF ───────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def csrf_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-CSRF-Token') or (request.json or {}).get('_csrf')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
            session['user'] = data['username']
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/csrf-token', methods=['GET'])
@login_required
def csrf_token():
    return jsonify({'token': get_csrf_token()})

@app.route('/logout', methods=['POST'])
@csrf_required
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/personnel', methods=['GET'])
@login_required
def get_personnel():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name, gender, blood, department, conditions FROM personnel ORDER BY id')
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {
            'id':         row[0],
            'name':       row[1],
            'gender':     row[2],
            'blood':      row[3],
            'department': row[4],
            'conditions': row[5].split('|') if row[5] else []
        }
        for row in rows
    ])

@app.route('/personnel/add', methods=['POST'])
@login_required
@csrf_required
def add_personnel():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'INSERT INTO personnel (name, gender, blood, department, conditions) VALUES (%s, %s, %s, %s, %s)',
        (
            data.get('name', ''),
            data.get('gender', ''),
            data.get('blood', ''),
            data.get('department', ''),
            '|'.join(data.get('conditions', []))
        )
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Personnel added successfully!'})

@app.route('/personnel/delete/<int:pid>', methods=['DELETE'])
@login_required
@csrf_required
def delete_personnel(pid):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM personnel WHERE id = %s', (pid,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Record not found'}), 404
    c.execute('DELETE FROM personnel WHERE id = %s', (pid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted successfully!'})

@app.route('/upload', methods=['POST'])
@login_required
@csrf_required
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))
    records = [
        (
            row.get('name', ''),
            row.get('gender', ''),
            row.get('blood', ''),
            row.get('department', ''),
            row.get('conditions', '')
        )
        for row in reader
    ]

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM personnel')
    psycopg2.extras.execute_batch(
        c,
        'INSERT INTO personnel (name, gender, blood, department, conditions) VALUES (%s, %s, %s, %s, %s)',
        records
    )
    conn.commit()
    conn.close()
    return jsonify({'message': f'{len(records)} records uploaded successfully!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f'Running at http://127.0.0.1:{port}')
    app.run(host='0.0.0.0', port=port, debug=debug)