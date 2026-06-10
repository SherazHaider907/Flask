from flask import Flask , request , redirect , url_for , session , Response


app = Flask(__name__)
app.secret_key = "supersecretkey" # Set a secret key for session management

# home page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '1234':
            session['username'] = username # Store the username in the session
            return redirect(url_for('welcome'))
        else:
            return Response('Invalid credentials', status=401, mimetype='text/plain')
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <input type="submit" value="Login">
        </form>
    '''

# welcome page
@app.route('/welcome')
def welcome():
    if 'username' in session:
        return f''' 
            <h1>Welcome, {session['username']}!</h1>
            <a href={url_for('logout')}>Logout</a>
        '''
    return redirect(url_for('login'))

# logout page
@app.route('/logout')
def logout():
    session.pop('username', None) # Remove the username from the session
    return redirect(url_for('login'))