from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
import os, csv, io, secrets, json
from datetime import datetime
import psycopg2, psycopg2.extras

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
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL environment variable is not set.')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return psycopg2.connect(database_url)

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Personnel table — extended with age, phone, address
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

    # Add new columns to existing table if upgrading
    for col, coltype in [('age','INTEGER'),('phone','TEXT'),('address','TEXT')]:
        c.execute(f'''
            DO $$ BEGIN
                ALTER TABLE personnel ADD COLUMN {col} {coltype};
            EXCEPTION WHEN duplicate_column THEN NULL;
            END $$;
        ''')

    # Visits / patient records table
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

    # Departments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id   SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Audit log table
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

    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()

    # Seed departments
    c.execute('SELECT COUNT(*) FROM departments')
    if c.fetchone()[0] == 0:
        depts = [('CHS',), ('COE',), ('CTE',), ('CBEA',), ('CAS',)]
        psycopg2.extras.execute_batch(c, 'INSERT INTO departments (name) VALUES (%s) ON CONFLICT DO NOTHING', depts)

    # Seed personnel
    c.execute('SELECT COUNT(*) FROM personnel')
    if c.fetchone()[0] == 0:
        records = [
            ('Ana Reyes',         32, 'Female', 'O+',  'CHS',  '09171234567', 'Laoag City',        'Hypertension|Diabetes'),
            ('Juan dela Cruz',    45, 'Male',   'A+',  'COE',  '09281234567', 'Batac City',        'Asthma'),
            ('Maria Santos',      28, 'Female', 'B+',  'CTE',  '09391234567', 'Paoay, Ilocos Norte','Allergies|Migraine'),
            ('Carlos Mendoza',    51, 'Male',   'AB+', 'CBEA', '09171239999', 'Sarrat, Ilocos Norte','Hypertension'),
            ('Liza Fernandez',    38, 'Female', 'O-',  'CAS',  '09281239999', 'Vintar, Ilocos Norte','Anemia'),
            ('Ramon Torres',      55, 'Male',   'A+',  'CHS',  '09391239999', 'Laoag City',        'Diabetes|Obesity'),
            ('Gloria Villanueva', 60, 'Female', 'B-',  'COE',  '09171230000', 'Bacarra, Ilocos Norte','Arthritis'),
            ('Eduardo Garcia',    47, 'Male',   'O+',  'CTE',  '09281230000', 'Batac City',        'Heart Disease'),
            ('Nora Bautista',     42, 'Female', 'A-',  'CBEA', '09391230000', 'Laoag City',        'Thyroid Disorder|Hypertension'),
            ('Miguel Ramos',      36, 'Male',   'AB-', 'CAS',  '09171231111', 'Piddig, Ilocos Norte','Gastritis'),
            ('Josie Aquino',      29, 'Female', 'O+',  'CHS',  '09281231111', 'Laoag City',        'Asthma|Allergies'),
            ('Andres Flores',     50, 'Male',   'B+',  'COE',  '09391231111', 'Batac City',        'Ulcer'),
            ('Cristina Lopez',    33, 'Female', 'A+',  'CTE',  '09171232222', 'Laoag City',        'Mental Health'),
            ('Roberto Cruz',      58, 'Male',   'O-',  'CBEA', '09281232222', 'Paoay, Ilocos Norte','Hypertension|Kidney Disease'),
            ('Teresita Ocampo',   44, 'Female', 'B+',  'CAS',  '09391232222', 'Vintar, Ilocos Norte','Diabetes'),
            ('Danilo Castillo',   39, 'Male',   'A+',  'CHS',  '09171233333', 'Batac City',        'Bronchitis'),
            ('Maribel Reyes',     27, 'Female', 'AB+', 'COE',  '09281233333', 'Laoag City',        'Migraine|Anemia'),
            ('Ernesto Salazar',   62, 'Male',   'O+',  'CTE',  '09391233333', 'Sarrat, Ilocos Norte','Liver Disease'),
            ('Rowena Pascual',    31, 'Female', 'A-',  'CBEA', '09171234444', 'Laoag City',        'Asthma'),
            ('Felix Navarro',     53, 'Male',   'B-',  'CAS',  '09281234444', 'Batac City',        'Heart Disease|Diabetes'),
        ]
        psycopg2.extras.execute_batch(
            c,
            'INSERT INTO personnel (name, age, gender, blood, department, phone, address, conditions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
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
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def csrf_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-CSRF-Token') or (request.json or {}).get('_csrf')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated

def audit(action, detail=''):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'INSERT INTO audit_log (username, action, detail, ip) VALUES (%s, %s, %s, %s)',
            (session.get('user', 'system'), action, detail, request.remote_addr)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

# ── AUTH ROUTES ───────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
            session['user'] = data['username']
            audit('LOGIN', f'Admin logged in from {request.remote_addr}')
            return jsonify({'success': True})
        audit('LOGIN_FAIL', f'Failed login attempt for "{data.get("username")}"')
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/csrf-token')
@login_required
def csrf_token():
    return jsonify({'token': get_csrf_token()})

@app.route('/logout', methods=['POST'])
@csrf_required
def logout():
    audit('LOGOUT')
    session.clear()
    return jsonify({'success': True})

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ── PERSONNEL ─────────────────────────────────────────────────────────────────

@app.route('/personnel')
@login_required
def get_personnel():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name, age, gender, blood, department, phone, address, conditions FROM personnel ORDER BY id')
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        'id': r[0], 'name': r[1], 'age': r[2], 'gender': r[3],
        'blood': r[4], 'department': r[5], 'phone': r[6], 'address': r[7],
        'conditions': r[8].split('|') if r[8] else []
    } for r in rows])

@app.route('/personnel/add', methods=['POST'])
@login_required
@csrf_required
def add_personnel():
    d = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'INSERT INTO personnel (name, age, gender, blood, department, phone, address, conditions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        (d.get('name',''), d.get('age'), d.get('gender',''), d.get('blood',''),
         d.get('department',''), d.get('phone',''), d.get('address',''),
         '|'.join(d.get('conditions',[])))
    )
    conn.commit()
    conn.close()
    audit('ADD_PERSONNEL', d.get('name',''))
    return jsonify({'message': 'Personnel added successfully!'})

@app.route('/personnel/update/<int:pid>', methods=['PUT'])
@login_required
@csrf_required
def update_personnel(pid):
    d = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM personnel WHERE id=%s', (pid,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    c.execute('''UPDATE personnel SET name=%s, age=%s, gender=%s, blood=%s,
                 department=%s, phone=%s, address=%s, conditions=%s WHERE id=%s''',
        (d.get('name',''), d.get('age'), d.get('gender',''), d.get('blood',''),
         d.get('department',''), d.get('phone',''), d.get('address',''),
         '|'.join(d.get('conditions',[])), pid))
    conn.commit()
    conn.close()
    audit('UPDATE_PERSONNEL', f'id={pid} name={d.get("name","")}')
    return jsonify({'message': 'Updated successfully!'})

@app.route('/personnel/delete/<int:pid>', methods=['DELETE'])
@login_required
@csrf_required
def delete_personnel(pid):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT name FROM personnel WHERE id=%s', (pid,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    c.execute('DELETE FROM personnel WHERE id=%s', (pid,))
    conn.commit()
    conn.close()
    audit('DELETE_PERSONNEL', f'id={pid} name={row[0]}')
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
    records = [(
        row.get('name',''), row.get('age') or None, row.get('gender',''),
        row.get('blood',''), row.get('department',''),
        row.get('phone',''), row.get('address',''), row.get('conditions','')
    ) for row in reader]
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM personnel')
    psycopg2.extras.execute_batch(
        c,
        'INSERT INTO personnel (name,age,gender,blood,department,phone,address,conditions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        records
    )
    conn.commit()
    conn.close()
    audit('UPLOAD_CSV', f'{len(records)} records')
    return jsonify({'message': f'{len(records)} records uploaded successfully!'})

# ── VISITS ────────────────────────────────────────────────────────────────────

@app.route('/personnel/<int:pid>/visits')
@login_required
def get_visits(pid):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, visit_date, reason, notes, created_at FROM visits WHERE personnel_id=%s ORDER BY visit_date DESC', (pid,))
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        'id': r[0], 'visit_date': str(r[1]), 'reason': r[2],
        'notes': r[3], 'created_at': str(r[4])
    } for r in rows])

@app.route('/personnel/<int:pid>/visits/add', methods=['POST'])
@login_required
@csrf_required
def add_visit(pid):
    d = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM personnel WHERE id=%s', (pid,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Personnel not found'}), 404
    c.execute(
        'INSERT INTO visits (personnel_id, visit_date, reason, notes) VALUES (%s,%s,%s,%s)',
        (pid, d.get('visit_date'), d.get('reason',''), d.get('notes',''))
    )
    conn.commit()
    conn.close()
    audit('ADD_VISIT', f'personnel_id={pid}')
    return jsonify({'message': 'Visit recorded!'})

@app.route('/visits/delete/<int:vid>', methods=['DELETE'])
@login_required
@csrf_required
def delete_visit(vid):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM visits WHERE id=%s', (vid,))
    conn.commit()
    conn.close()
    audit('DELETE_VISIT', f'visit_id={vid}')
    return jsonify({'message': 'Visit deleted!'})

# ── DEPARTMENTS ───────────────────────────────────────────────────────────────

@app.route('/departments')
@login_required
def get_departments():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name FROM departments ORDER BY name')
    rows = c.fetchall()
    conn.close()
    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

@app.route('/departments/add', methods=['POST'])
@login_required
@csrf_required
def add_department():
    name = (request.json or {}).get('name','').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO departments (name) VALUES (%s)', (name,))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Department already exists'}), 409
    conn.close()
    audit('ADD_DEPT', name)
    return jsonify({'message': f'Department "{name}" added!'})

@app.route('/departments/delete/<int:did>', methods=['DELETE'])
@login_required
@csrf_required
def delete_department(did):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT name FROM departments WHERE id=%s', (did,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    c.execute('DELETE FROM departments WHERE id=%s', (did,))
    conn.commit()
    conn.close()
    audit('DELETE_DEPT', row[0])
    return jsonify({'message': 'Department deleted!'})

# ── AUDIT LOG ─────────────────────────────────────────────────────────────────

@app.route('/audit-log')
@login_required
def get_audit_log():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, username, action, detail, ip, created_at FROM audit_log ORDER BY created_at DESC LIMIT 200')
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        'id': r[0], 'username': r[1], 'action': r[2],
        'detail': r[3], 'ip': r[4], 'created_at': str(r[5])
    } for r in rows])

# ── EXPORT ────────────────────────────────────────────────────────────────────

@app.route('/export/personnel')
@login_required
def export_personnel():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name, age, gender, blood, department, phone, address, conditions FROM personnel ORDER BY id')
    rows = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','name','age','gender','blood','department','phone','address','conditions'])
    for r in rows:
        writer.writerow(r)
    audit('EXPORT_CSV', f'{len(rows)} records')
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=personnel_export.csv'}
    )

@app.route('/export/visits')
@login_required
def export_visits():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT v.id, p.name, v.visit_date, v.reason, v.notes
                 FROM visits v JOIN personnel p ON p.id=v.personnel_id
                 ORDER BY v.visit_date DESC''')
    rows = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['visit_id','personnel_name','visit_date','reason','notes'])
    for r in rows:
        writer.writerow(r)
    audit('EXPORT_VISITS_CSV', f'{len(rows)} visits')
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=visits_export.csv'}
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
