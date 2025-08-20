from estudo import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    password = db.Column(db.String(60), nullable=False)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    pets = db.relationship('Pet', backref='customer', lazy=True)
    appointments = db.relationship('Appointment', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name!r}>'

class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=True)
    breed = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='pet', lazy=True)

    def __repr__(self):
        return f'<Pet {self.name!r}>'

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name!r}: {self.price}>'

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Scheduled')

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    pet_name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    def __repr__(self):
        return (f'<Appointment {self.id} - Pet: {self.pet.name!r} - '
                f'DateTime: {self.date_time}>')
