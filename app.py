from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return "<p>This is the about page.</p>"

@app.route("/contact")
def contact():
    return "<p>Contact us</p>"

