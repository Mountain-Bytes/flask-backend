

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    pen_name = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, first_name, last_name, password, dob, email, phone_number, pen_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pen_name = pen_name if pen_name else first_name
        self.password = password
        self.dob = dob
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'


