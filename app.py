from flask import Flask, Response, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
from contextlib import contextmanager
import csv
import io
import os
import secrets

import psycopg2
import psycopg2.extras

# ── APP SETUP ─────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR)

app.secret_key = os.environ.get('SECRET_KEY', 'mmsu_medical_dashboard_secret_2024_CHANGE_IN_PRODUCTION')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'mmsu2024')

# ── DATABASE ──────────────────────────────────────────────────────────────────

def _get_db_url():
    url = os.environ.get('DATABASE_URL')
    if not url:
        raise RuntimeError('DATABASE_URL environment variable is not set.')
    # Heroku/Railway uses the legacy postgres:// scheme; psycopg2 needs postgresql://
    return url.replace('postgres://', 'postgresql://', 1)

@contextmanager
def get_db():
    """Context manager that opens a connection and always closes it."""
    conn = psycopg2.connect(_get_db_url())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS personnel (
                id         SERIAL PRIMARY KEY,
                name       TEXT,
                age        INTEGER,
                gender     TEXT,
                blood      TEXT,
                department TEXT,
                phone      TEXT,
                address    TEXT,
                conditions TEXT
            )
        ''')

        # Migrate older tables that predate the age/phone/address columns
        for col, coltype in [('age', 'INTEGER'), ('phone', 'TEXT'), ('address', 'TEXT')]:
            c.execute(f'''
                DO $$ BEGIN
                    ALTER TABLE personnel ADD COLUMN {col} {coltype};
                EXCEPTION WHEN duplicate_column THEN NULL;
                END $$;
            ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id           SERIAL PRIMARY KEY,
                personnel_id INTEGER REFERENCES personnel(id) ON DELETE CASCADE,
                visit_date   DATE NOT NULL,
                reason       TEXT,
                notes        TEXT,
                created_at   TIMESTAMP DEFAULT NOW()
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id   SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id         SERIAL PRIMARY KEY,
                username   TEXT,
                action     TEXT,
                detail     TEXT,
                ip         TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')

init_db()

# ── HELPERS ───────────────────────────────────────────────────────────────────

def row_to_person(r):
    return {
        'id': r[0], 'name': r[1], 'age': r[2], 'gender': r[3],
        'blood': r[4], 'department': r[5], 'phone': r[6], 'address': r[7],
        'conditions': r[8].split('|') if r[8] else [],
    }

def person_params(d):
    """Extract and normalise personnel fields from a request payload."""
    return (
        d.get('name', ''),
        d.get('age'),
        d.get('gender', ''),
        d.get('blood', ''),
        d.get('department', ''),
        d.get('phone', ''),
        d.get('address', ''),
        '|'.join(d.get('conditions', [])),
    )

def csv_response(rows, headers, filename):
    """Build a CSV download response from a list of rows."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    writer.writerows(rows)
    return Response(
        buf.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )

def audit(action, detail=''):
    """Write an entry to the audit log. Silently swallows errors."""
    try:
        with get_db() as conn:
            conn.cursor().execute(
                'INSERT INTO audit_log (username, action, detail, ip) VALUES (%s, %s, %s, %s)',
                (session.get('user', 'system'), action, detail, request.remote_addr),
            )
    except Exception:
        pass

# ── AUTH / CSRF DECORATORS ────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def csrf_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-CSRF-Token') or (request.json or {}).get('_csrf')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated

def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

# ── AUTH ROUTES ───────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json or {}
        if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
            session['user'] = data['username']
            audit('LOGIN', f'Admin logged in from {request.remote_addr}')
            return jsonify({'success': True})
        audit('LOGIN_FAIL', f'Failed login attempt for "{data.get("username")}"')
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@csrf_required
def logout():
    audit('LOGOUT')
    session.clear()
    return jsonify({'success': True})

@app.route('/csrf-token')
@login_required
def csrf_token():
    return jsonify({'token': get_csrf_token()})

# ── PERSONNEL ─────────────────────────────────────────────────────────────────

@app.route('/personnel')
@login_required
def get_personnel():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, age, gender, blood, department, phone, address, conditions FROM personnel ORDER BY id')
        return jsonify([row_to_person(r) for r in c.fetchall()])

@app.route('/personnel/add', methods=['POST'])
@login_required
@csrf_required
def add_personnel():
    d = request.json or {}
    with get_db() as conn:
        conn.cursor().execute(
            'INSERT INTO personnel (name, age, gender, blood, department, phone, address, conditions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
            person_params(d),
        )
    audit('ADD_PERSONNEL', d.get('name', ''))
    return jsonify({'message': 'Personnel added successfully!'})

@app.route('/personnel/update/<int:pid>', methods=['PUT'])
@login_required
@csrf_required
def update_personnel(pid):
    d = request.json or {}
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM personnel WHERE id = %s', (pid,))
        if not c.fetchone():
            return jsonify({'error': 'Not found'}), 404
        c.execute(
            '''UPDATE personnel
               SET name=%s, age=%s, gender=%s, blood=%s,
                   department=%s, phone=%s, address=%s, conditions=%s
               WHERE id=%s''',
            (*person_params(d), pid),
        )
    audit('UPDATE_PERSONNEL', f'id={pid} name={d.get("name", "")}')
    return jsonify({'message': 'Updated successfully!'})

@app.route('/personnel/delete/<int:pid>', methods=['DELETE'])
@login_required
@csrf_required
def delete_personnel(pid):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT name FROM personnel WHERE id = %s', (pid,))
        row = c.fetchone()
        if not row:
            return jsonify({'error': 'Not found'}), 404
        c.execute('DELETE FROM personnel WHERE id = %s', (pid,))
    audit('DELETE_PERSONNEL', f'id={pid} name={row[0]}')
    return jsonify({'message': 'Deleted successfully!'})

@app.route('/upload', methods=['POST'])
@login_required
@csrf_required
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
    records = [
        (
            row.get('name', ''), row.get('age') or None, row.get('gender', ''),
            row.get('blood', ''), row.get('department', ''),
            row.get('phone', ''), row.get('address', ''), row.get('conditions', ''),
        )
        for row in reader
    ]

    with get_db() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM personnel')
        psycopg2.extras.execute_batch(
            c,
            'INSERT INTO personnel (name, age, gender, blood, department, phone, address, conditions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
            records,
        )

    audit('UPLOAD_CSV', f'{len(records)} records')
    return jsonify({'message': f'{len(records)} records uploaded successfully!'})

# ── VISITS ────────────────────────────────────────────────────────────────────

@app.route('/personnel/<int:pid>/visits')
@login_required
def get_visits(pid):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            'SELECT id, visit_date, reason, notes, created_at FROM visits WHERE personnel_id = %s ORDER BY visit_date DESC',
            (pid,),
        )
        return jsonify([
            {'id': r[0], 'visit_date': str(r[1]), 'reason': r[2], 'notes': r[3], 'created_at': str(r[4])}
            for r in c.fetchall()
        ])

@app.route('/personnel/<int:pid>/visits/add', methods=['POST'])
@login_required
@csrf_required
def add_visit(pid):
    d = request.json or {}
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM personnel WHERE id = %s', (pid,))
        if not c.fetchone():
            return jsonify({'error': 'Personnel not found'}), 404
        c.execute(
            'INSERT INTO visits (personnel_id, visit_date, reason, notes) VALUES (%s, %s, %s, %s)',
            (pid, d.get('visit_date'), d.get('reason', ''), d.get('notes', '')),
        )
    audit('ADD_VISIT', f'personnel_id={pid}')
    return jsonify({'message': 'Visit recorded!'})

@app.route('/visits/delete/<int:vid>', methods=['DELETE'])
@login_required
@csrf_required
def delete_visit(vid):
    with get_db() as conn:
        conn.cursor().execute('DELETE FROM visits WHERE id = %s', (vid,))
    audit('DELETE_VISIT', f'visit_id={vid}')
    return jsonify({'message': 'Visit deleted!'})

# ── DEPARTMENTS ───────────────────────────────────────────────────────────────

@app.route('/departments')
@login_required
def get_departments():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name FROM departments ORDER BY name')
        return jsonify([{'id': r[0], 'name': r[1]} for r in c.fetchall()])

@app.route('/departments/add', methods=['POST'])
@login_required
@csrf_required
def add_department():
    name = (request.json or {}).get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    try:
        with get_db() as conn:
            conn.cursor().execute('INSERT INTO departments (name) VALUES (%s)', (name,))
    except psycopg2.errors.UniqueViolation:
        return jsonify({'error': 'Department already exists'}), 409
    audit('ADD_DEPT', name)
    return jsonify({'message': f'Department "{name}" added!'})

@app.route('/departments/delete/<int:did>', methods=['DELETE'])
@login_required
@csrf_required
def delete_department(did):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT name FROM departments WHERE id = %s', (did,))
        row = c.fetchone()
        if not row:
            return jsonify({'error': 'Not found'}), 404
        c.execute('DELETE FROM departments WHERE id = %s', (did,))
    audit('DELETE_DEPT', row[0])
    return jsonify({'message': 'Department deleted!'})

# ── AUDIT LOG ─────────────────────────────────────────────────────────────────

@app.route('/audit-log')
@login_required
def get_audit_log():
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            'SELECT id, username, action, detail, ip, created_at FROM audit_log ORDER BY created_at DESC LIMIT 200'
        )
        return jsonify([
            {'id': r[0], 'username': r[1], 'action': r[2], 'detail': r[3], 'ip': r[4], 'created_at': str(r[5])}
            for r in c.fetchall()
        ])

# ── EXPORT ────────────────────────────────────────────────────────────────────

@app.route('/export/personnel')
@login_required
def export_personnel():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, age, gender, blood, department, phone, address, conditions FROM personnel ORDER BY id')
        rows = c.fetchall()
    audit('EXPORT_CSV', f'{len(rows)} records')
    return csv_response(rows, ['id', 'name', 'age', 'gender', 'blood', 'department', 'phone', 'address', 'conditions'], 'personnel_export.csv')

@app.route('/export/visits')
@login_required
def export_visits():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT v.id, p.name, v.visit_date, v.reason, v.notes
            FROM visits v
            JOIN personnel p ON p.id = v.personnel_id
            ORDER BY v.visit_date DESC
        ''')
        rows = c.fetchall()
    audit('EXPORT_VISITS_CSV', f'{len(rows)} visits')
    return csv_response(rows, ['visit_id', 'personnel_name', 'visit_date', 'reason', 'notes'], 'visits_export.csv')

# ── ENTRYPOINT ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') != 'production',
    )