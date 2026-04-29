from flask import Flask, Response, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
from contextlib import contextmanager
import csv
import io
import os
import secrets
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

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

# ── PDF EXPORT ────────────────────────────────────────────────────────────────

@app.route('/personnel/<int:pid>/pdf')
@login_required
def export_personnel_pdf(pid):
    if not REPORTLAB_AVAILABLE:
        return jsonify({'error': 'reportlab is not installed on the server. Run: pip install reportlab'}), 500

    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, age, gender, blood, department, phone, address, conditions FROM personnel WHERE id = %s', (pid,))
        row = c.fetchone()
        if not row:
            return jsonify({'error': 'Personnel not found'}), 404
        p = row_to_person(row)

        # Fetch visits
        c.execute(
            'SELECT visit_date, reason, notes FROM visits WHERE personnel_id = %s ORDER BY visit_date DESC LIMIT 10',
            (pid,)
        )
        visits = c.fetchall()

    audit('EXPORT_PDF', f'id={pid} name={p["name"]}')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    # ── Colours & styles ──
    GREEN       = colors.HexColor('#1a7a3c')
    GREEN_LIGHT = colors.HexColor('#e8f5ee')
    GOLD        = colors.HexColor('#d4b84a')
    DARK        = colors.HexColor('#111111')
    GREY        = colors.HexColor('#555555')
    LIGHT_GREY  = colors.HexColor('#f6f7f6')
    BORDER      = colors.HexColor('#e0e0e0')
    RED_BG      = colors.HexColor('#fdecea')
    RED_TEXT    = colors.HexColor('#c0392b')

    styles = getSampleStyleSheet()

    def style(name, **kw):
        s = ParagraphStyle(name, parent=styles['Normal'], **kw)
        return s

    title_style    = style('Title',    fontSize=20, textColor=DARK,  fontName='Helvetica-Bold', spaceAfter=2)
    dept_style     = style('Dept',     fontSize=11, textColor=GREY,  fontName='Helvetica')
    label_style    = style('Label',    fontSize=8,  textColor=GREY,  fontName='Helvetica-Bold')
    value_style    = style('Value',    fontSize=12, textColor=DARK,  fontName='Helvetica-Bold')
    value_sm       = style('ValueSm',  fontSize=11, textColor=DARK,  fontName='Helvetica')
    section_style  = style('Section',  fontSize=8,  textColor=GREY,  fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
    footer_style   = style('Footer',   fontSize=8,  textColor=GREY,  fontName='Helvetica', alignment=TA_CENTER)
    visit_date_s   = style('VDate',    fontSize=8,  textColor=GREEN, fontName='Helvetica-Bold')
    visit_reason_s = style('VReason',  fontSize=11, textColor=DARK,  fontName='Helvetica-Bold')
    visit_notes_s  = style('VNotes',   fontSize=10, textColor=GREY,  fontName='Helvetica')

    initials = ''.join(w[0] for w in p['name'].split() if w)[:2].upper()

    # ── Build story ──
    story = []
    page_w = A4[0] - 4*cm  # usable width

    # Header row: [avatar] [name \n dept] [MMSU Medical \n subtitle]
    name_dept_combined = style('NameDept', fontSize=11, textColor=GREY, fontName='Helvetica',
                                leading=28, leftIndent=10)
    name_para = Paragraph(
        f'<font name="Helvetica-Bold" size="20" color="#111111">{p["name"]}</font><br/>'
        f'<font name="Helvetica" size="11" color="#555555">{p["department"]} Department</font>',
        name_dept_combined
    )

    logo_combined = style('LogoCombined', fontSize=9, textColor=GREY, fontName='Helvetica',
                           alignment=TA_RIGHT, leading=20)
    logo_para = Paragraph(
        f'<font name="Helvetica-Bold" size="13" color="#1a7a3c">MMSU Medical</font><br/>'
        f'<font name="Helvetica" size="9" color="#555555">Health Records System</font>',
        logo_combined
    )

    header_data = [[
        Paragraph(f'<font color="#d4b84a"><b>{initials}</b></font>',
                  style('Av', fontSize=22, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=GOLD)),
        name_para,
        logo_para,
    ]]
    header_table = Table(header_data, colWidths=[2*cm, 10*cm, 5*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(0,0), GREEN),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('ALIGN',         (0,0),(0,0), 'CENTER'),
        ('ALIGN',         (2,0),(2,0), 'RIGHT'),
        ('TOPPADDING',    (0,0),(-1,-1), 14),
        ('BOTTOMPADDING', (0,0),(-1,-1), 14),
        ('LEFTPADDING',   (0,0),(0,0), 0),
        ('RIGHTPADDING',  (0,0),(0,0), 0),
        ('LEFTPADDING',   (2,0),(2,0), 0),
        ('RIGHTPADDING',  (2,0),(2,0), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=12, spaceBefore=10))

    # Info grid
    def info_cell(label, value, blood=False):
        val_color = GOLD if blood else DARK
        return [
            Paragraph(label, label_style),
            Paragraph(str(value) if value else '—', style('VC', fontSize=12, textColor=val_color, fontName='Helvetica-Bold')),
        ]

    age_val  = f'{p["age"]} yrs' if p.get('age') else '—'
    grid_data = [
        [info_cell('GENDER', p.get('gender') or '—'),  info_cell('BLOOD TYPE', p.get('blood') or '—', blood=True)],
        [info_cell('AGE',    age_val),                  info_cell('PHONE', p.get('phone') or '—')],
    ]

    def make_cell(items):
        tbl = Table([[i] for i in items], colWidths=[(page_w/2 - 0.3*cm)])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), LIGHT_GREY),
            ('BOX',        (0,0),(-1,-1), 0.5, BORDER),
            ('ROUNDEDCORNERS', [6]),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING',   (0,0),(-1,-1), 12),
            ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ]))
        return tbl

    grid_table_data = [
        [make_cell(grid_data[0][0]), make_cell(grid_data[0][1])],
        [make_cell(grid_data[1][0]), make_cell(grid_data[1][1])],
    ]
    grid_table = Table(grid_table_data, colWidths=[page_w/2 - 0.15*cm, page_w/2 - 0.15*cm], hAlign='LEFT')
    grid_table.setStyle(TableStyle([
        ('VALIGN',      (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0),(-1,-1), 0),
        ('RIGHTPADDING',(0,0),(-1,-1), 0),
        ('TOPPADDING',  (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('INNERGRID',   (0,0),(-1,-1), 0, colors.white),
        ('BOX',         (0,0),(-1,-1), 0, colors.white),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 6))

    # Address full-width
    addr_cell = Table([
        [Paragraph('ADDRESS', label_style)],
        [Paragraph(p.get('address') or '—', value_sm)],
    ], colWidths=[page_w])
    addr_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), LIGHT_GREY),
        ('BOX',          (0,0),(-1,-1), 0.5, BORDER),
        ('TOPPADDING',   (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',  (0,0),(-1,-1), 12),
        ('RIGHTPADDING', (0,0),(-1,-1), 12),
    ]))
    story.append(addr_cell)

    # Conditions
    story.append(Paragraph('RECORDED CONDITIONS', section_style))
    HIGH_RISK = ['Hypertension','Diabetes','Asthma','Heart Disease','Tuberculosis','Cancer','HIV/AIDS','Epilepsy']
    if p['conditions']:
        cond_cells = []
        for cond in p['conditions']:
            is_high = cond in HIGH_RISK
            bg  = RED_BG   if is_high else LIGHT_GREY
            txt = RED_TEXT if is_high else DARK
            border = colors.HexColor('#f5c6c6') if is_high else BORDER
            cell = Table([[Paragraph(cond, style('Pill', fontSize=10, textColor=txt, fontName='Helvetica-Bold'))]],
                         colWidths=[len(cond)*6 + 24])
            cell.setStyle(TableStyle([
                ('BACKGROUND',   (0,0),(-1,-1), bg),
                ('BOX',          (0,0),(-1,-1), 0.5, border),
                ('TOPPADDING',   (0,0),(-1,-1), 4),
                ('BOTTOMPADDING',(0,0),(-1,-1), 4),
                ('LEFTPADDING',  (0,0),(-1,-1), 10),
                ('RIGHTPADDING', (0,0),(-1,-1), 10),
            ]))
            cond_cells.append(cell)
        # Lay pills in a row table
        pills_table = Table([cond_cells], colWidths=[len(c)*6+24 for c in p['conditions']], hAlign='LEFT')
        pills_table.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),
                                         ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        story.append(pills_table)
    else:
        story.append(Paragraph('No conditions recorded.', style('NoCond', fontSize=11, textColor=GREY, fontName='Helvetica')))

    # Recent Visits
    if visits:
        story.append(Paragraph('RECENT VISITS', section_style))
        for vdate, reason, notes in visits:
            visit_data = [
                [Paragraph(str(vdate), visit_date_s)],
                [Paragraph(reason or 'General Visit', visit_reason_s)],
            ]
            if notes:
                visit_data.append([Paragraph(notes, visit_notes_s)])
            vt = Table(visit_data, colWidths=[page_w - 0.3*cm])
            vt.setStyle(TableStyle([
                ('BACKGROUND',   (0,0),(-1,-1), LIGHT_GREY),
                ('BOX',          (0,0),(-1,-1), 0.5, BORDER),
                ('TOPPADDING',   (0,0),(-1,-1), 6),
                ('BOTTOMPADDING',(0,0),(-1,-1), 6),
                ('LEFTPADDING',  (0,0),(-1,-1), 12),
                ('RIGHTPADDING', (0,0),(-1,-1), 12),
            ]))
            story.append(vt)
            story.append(Spacer(1, 5))

    # Footer
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=8))
    now_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    story.append(Paragraph(f'Generated on {now_str}  ·  MMSU Medical Health Records  ·  Confidential', footer_style))

    doc.build(story)
    buf.seek(0)
    safe_name = p['name'].replace(' ', '_')
    return Response(
        buf.getvalue(),
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={safe_name}_medical_record.pdf'}
    )


# ── ENTRYPOINT ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') != 'production',
    )