from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from estudo.models import Customer
from validate_docbr import CPF as CPFValidator

from estudo import db, bcrypt
from estudo.models import User

cpf_validator_lib = CPFValidator()

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'Funcionário'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def save(self):
        hashed = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        user = User(
            name=self.name.data,
            username=self.username.data,
            email=self.email.data,
            role=self.role.data,
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        return user
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.password.data.encode('utf-8')):
                return user
            else:
                raise Exception('Invalid username or password!')
        else:
            raise Exception('Invalid username or password!')
        

class ScheduleForm(FlaskForm):
    date_time = DateTimeField('DateTime', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    service = SelectField('Service', coerce=int, validators=[DataRequired()])
    pet = SelectField('Pet', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Confirm')


class CustomerForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefone')
    address = StringField('Endereço')
    submit = SubmitField('Confirmar')

    def validate_cpf(self, field):
        raw = ''.join(ch for ch in field.data if ch.isdigit())
        if len(raw) != 11:
            raise ValidationError('CPF deve ter 11 dígitos.')
        if cpf_validator_lib:
            if not cpf_validator_lib.validate(raw):
                raise ValidationError('CPF inválido.')
        # Checa unicidade
        existing = Customer.query.filter_by(cpf=field.data).first()
        if existing:
            raise ValidationError('CPF já cadastrado.')


class PetForm(FlaskForm):
    name = StringField('Nome do Pet', validators=[DataRequired()])
    species = StringField('Espécie', validators=[DataRequired()])
    breed = StringField('Raça')
    age = IntegerField('Idade')
    customer_id = SelectField('Cliente (CPF - Nome)', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cadastrar')