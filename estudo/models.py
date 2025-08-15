from estudo import db
from datetime import datetime

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, default = datetime.utcnow())
    name = db.Column(db.String, nullable = True)
    email = db.Column(db.String, nullable = True)
    description = db.Column(db.String, nullable = True)
    message = db.Column(db.String, nullable = True)
    