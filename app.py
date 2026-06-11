from flask import Flask, request, redirect, url_for, session, render_template


app = Flask(__name__)
app.secret_key = 'secret-key'


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == '123':
        session['username'] = username
        return redirect(url_for('welcome'))

    return ('Invalid credentials', 401)


@app.route('/welcome')
def welcome():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
