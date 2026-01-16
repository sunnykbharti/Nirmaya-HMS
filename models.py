from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    flag = db.Column(db.String(200), default="Inactive")


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    uhid = db.Column(db.String(200), nullable = False, unique = True)
    aadhar = db.Column(db.Integer, nullable = False, unique = True)
    city = db.Column(db.String(200), nullable = False)
    state = db.Column(db.String(200), nullable = False)
    mobile = db.Column(db.Integer, nullable = False)
    emergency = db.Column(db.Integer, nullable = False)
    doctor = db.Column(db.String(200), nullable = False)
    department = db.Column(db.String(200), nullable = False)
    docid = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Integer, nullable = False)
    #doctor = db.Column(db.Integer, db.ForeignKey('Doctor.id'))


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    imcid = db.Column(db.String(200), nullable = False, unique = True)
    aadhar = db.Column(db.Integer, nullable = False, unique = True)
    city = db.Column(db.String(200), nullable = False)
    state = db.Column(db.String(200), nullable = False)
    flag=db.Column(db.String(200), default="Inactive")


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    aadhar = db.Column(db.Integer, nullable = False, unique = True)
    city = db.Column(db.String(200), nullable = False)
    state = db.Column(db.String(200), nullable = False)

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    aadhar = db.Column(db.Integer, nullable = False, unique = True)
    city = db.Column(db.String(200), nullable = False)
    state = db.Column(db.String(200), nullable = False)
