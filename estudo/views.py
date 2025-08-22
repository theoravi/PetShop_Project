from estudo import app, db
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Appointment, Pet, Customer, User
from estudo.forms import (
    LoginForm,
    ScheduleForm,
    CustomerForm,
    UserForm,
    PetForm
)

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
        except Exception:
            flash('Usuário ou senha inválidos!', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    form = ScheduleForm()
    customers = Customer.query.order_by(Customer.name).all()
    form.customer_id.choices = [(c.id, c.name) for c in customers]
    form.pet.choices = [(p.id, f"{p.name} ({p.customer.name})") for c in customers for p in c.pets]

    if form.validate_on_submit():
        customer_id = form.customer_id.data
        pet_id = form.pet.data
        pet_obj = Pet.query.get(pet_id)
        if not pet_obj or pet_obj.customer_id != customer_id:
            flash('Pet inválido para o cliente selecionado.', 'danger')
            return redirect(url_for('appointments'))

        new_appt = Appointment(
            date_time=form.date_time.data,
            service_name=form.service_name.data,
            price=float(form.price.data),
            customer_id=customer_id,
            pet_id=pet_id,
            pet_name=pet_obj.name,
            status='Scheduled'
        )
        db.session.add(new_appt)
        db.session.commit()
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('appointments'))

    appointments_list = Appointment.query.filter_by(customer_id=current_user.id).all()
    pets_by_customer = {c.id: [{'id': p.id, 'name': p.name} for p in c.pets] for c in customers}
    return render_template('appointments.html',
                           form=form,
                           appointments=appointments_list,
                           customers=customers,
                           pets_dict=pets_by_customer)

    # lista exibida (apenas os agendamentos do usuário logado; adapte se for admin)
    appointments_list = Appointment.query.filter_by(customer_id=current_user.id).all()

    # montar mapa pets por cliente para o JS
    pets_by_customer = {}
    for c in customers:
        pets_by_customer[c.id] = [{'id': p.id, 'name': p.name} for p in c.pets]

    return render_template(
        'appointments.html',
        appointments=appointments_list,
        form=form,
        customers=customers,
        pets_dict=pets_by_customer
    )

@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    form = CustomerForm()
    if form.validate_on_submit():
        cpf_raw = ''.join(ch for ch in form.cpf.data if ch.isdigit())
        cpf_to_store = cpf_raw

        new_customer = Customer(
            cpf=cpf_to_store,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('customers'))

    return render_template('customers.html', form=form)

@app.route('/employees', methods=['GET', 'POST'])
@login_required
def employees():
    if not current_user.is_admin:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('appointments'))

    form = UserForm()
    if form.validate_on_submit():
        form.save()
        flash('Funcionário cadastrado com sucesso!', 'success')
        return redirect(url_for('employees'))

    return render_template('employees.html', form=form)

@app.route('/pets', methods=['GET', 'POST'])
@login_required
def pets():
    form = PetForm()
    customers = Customer.query.order_by(Customer.name).all()
    form.customer_id.choices = [(c.id, f"{c.cpf} - {c.name}") for c in customers]

    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            breed=form.breed.data,
            age=form.age.data,
            customer_id=form.customer_id.data
        )
        db.session.add(pet)
        db.session.commit()
        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('pets'))

    return render_template('pets.html', form=form)
