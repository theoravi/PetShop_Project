from estudo import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, login_required, logout_user, current_user

from estudo.forms import UserForm, LoginForm

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('TODO'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))