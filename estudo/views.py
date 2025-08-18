from estudo import app
from flask import render_template, url_for

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')