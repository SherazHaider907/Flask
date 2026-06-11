from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret-key'

@app.route('/')
def student_profile():
    return render_template(
        'profile.html',
        name='John Doe',
        is_Topper=True,
        major='Computer Science',
        subjects=['Math', 'Physics', 'Chemistry']
    )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == '123':
        session['username'] = username
        return redirect(url_for('welcome'))

    return render_template('login.html', error='Invalid credentials. Please try again.')

@app.route('/welcome')
def welcome():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=username)
