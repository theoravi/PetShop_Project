from estudo import app
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Appointment
from estudo.forms import UserForm, LoginForm

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)
            return redirect(url_for('appointments'))
        except Exception as e:
            flash('Invalid username or password!', 'danger')
            print(e)
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# @app.route('/management/')
# @login_required
# def management():
#     # caso queira, recupere agendamentos do banco:
#     # agendamentos = Appointment.query.filter_by(user_id=current_user.id).all()
#     return render_template('management.html', user=current_user)

@app.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.filter_by(customer_id=current_user.id).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/employees')
@login_required
def employees():
    # if not current_user.role != 'admin':
    #     return redirect(url_for('appointments'))
    return render_template('employees.html')

@app.route('/pets')
@login_required
def pets():
    return render_template('pets.html')

@app.route('/customers')
@login_required
def customers():
    return render_template('customers.html')
