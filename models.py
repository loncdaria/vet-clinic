from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import hashlib, binascii

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))

    def __repr__(self):
        return f'User {self.name}'
    
    def get_hash_password(self):
        """Hash a password for storing"""
        os_urandom_static=b'ID_\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user."""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, nullable=False)
    vetId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)


class Owner(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Integer(), nullable=False)

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)

class Vet(db.Model):
    __tablename__ = 'vet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Integer(), nullable=False)
