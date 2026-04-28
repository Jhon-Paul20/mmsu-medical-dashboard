from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mmsu_medical_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
        return redirect(url_for('overview'))
    return redirect(url_for('login'))

@app.route('/overview')
def overview():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    stats = {'total_personnel': 20, 'male_percent': 50.0, 'female_percent': 50.0, 'common_blood': 'O+'}
    blood_types = {'O+': 4, 'A+': 4, 'B+': 3, 'AB+': 2, 'O-': 2, 'B-': 2, 'A-': 2, 'AB-': 1}
    dept_counts = {'Nursing': 8, 'Pediatrics': 5, 'Radiology': 4, 'Admin': 3}
    risk_data = {'High Risk': 15, 'Stable': 85}
    
    return render_template('index.html', stats=stats, blood_types=blood_types, dept_counts=dept_counts, risk_data=risk_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)