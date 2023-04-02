from utils.db import db

class Tarea(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    titulo=db.Column(db.String(100))
    descripcion=db.Column(db.String(200))
    fecha=db.Column(db.Date)
    email=db.Column(db.String(200))

    def __init__(self,id, titulo, descripcion, fecha, email):
        self.id=id
        self.titulo=titulo
        self.descripcion=descripcion
        self.fecha=fecha
        self.email=email
        


