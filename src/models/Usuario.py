from utils.db import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))
    

    def __init__(self, id, email, password, tipo):
        self.id_usuario=id
        self.email=email
        self.password=password
        