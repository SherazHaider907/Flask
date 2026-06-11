from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def student_profile():
    return render_template('profile.html',
    name='John Doe', 
    is_Topper=True, 
    major='Computer Science',
    subjects=['Math', 'Physics', 'Chemistry']
    )