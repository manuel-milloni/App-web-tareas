from flask import Blueprint, render_template, request, flash, url_for, redirect
from utils.db import db
from models.Tarea import Tarea
from models.Usuario import Usuario
from logging import exception
from flask_login import login_user, logout_user, login_required, current_user
from utils.log_manager import login_manager_app
from datetime import date


rutas=Blueprint("rutas", __name__)

@login_manager_app.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=id).first()
    


@rutas.route('/')
def home():
    
    return render_template('index.html')

@rutas.route('/nuevo_usuario')
def nuevo_usuario():
    return render_template('registro.html')

@rutas.route('/registro_usuario', methods=["POST"])
def add_usuario():
    try:
        email_ingresado=request.form['email']
        password_ingresado=request.form['pass']
        password_ingresado_2=request.form['pass_2']
        #Valida que las password sean iguales
        if password_ingresado!=password_ingresado_2:  
            flash("Las contraseñas deben coincidir")
            return redirect(url_for('rutas.nuevo_usuario'))
        elif email_ingresado=="" or password_ingresado=="" or password_ingresado_2=="":
            flash("Debe completar todos los campos")
            return(redirect(url_for('rutas.nuevo_usuario')))
        else:
            usuario=Usuario.query.filter_by(email=email_ingresado).first()
            #Valida que el email ingresado no se encuentre en la base de datos
            if usuario==None:
                nuevo_usuario=Usuario(None, email_ingresado, password_ingresado)
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash("Usuario registrado exitosamente")
                return redirect(url_for('rutas.home'))
            else:
                flash("Error: el email ya se encuentra registrado")
                return redirect(url_for('rutas.home'))
    except Exception:
        exception("Error")
        return 500
    
@rutas.route('/login', methods=['POST'])
def login():
    email=request.form['email']
    password=request.form['password']
    usuario=Usuario.query.filter_by(email=email).first()
    if usuario!=None:
        if usuario.password==password:
            login_user(usuario)
            return redirect(url_for('rutas.tareas'))
            
            
        else:
            flash("Usuario o password incorrecto")
            return redirect(url_for('rutas.home'))
    else:
        flash("Usuario o password incorrecto")
        return redirect(url_for('rutas.home'))
    
@rutas.route('/tareas')
@login_required
def tareas():
    tareas=Tarea.query.filter_by(email=current_user.email)
    lista_tareas=[]
    for tarea in tareas:
        lista_tareas.append(tarea)
    

    return render_template('auth/tareas.html', lista_tareas=lista_tareas)

@rutas.route('/tareas/agregar_tarea', methods=['POST'])
def nueva_tarea():
    try:
        titulo=request.form['title']
        descripcion=request.form['descripcion']
        fecha=date.today()
        if titulo!="" and descripcion!="":
            tarea_nueva=Tarea(None, titulo, descripcion,fecha, current_user.email)
            db.session.add(tarea_nueva)
            db.session.commit()
            flash("Tarea agregada exitosamente")
            return redirect(url_for('rutas.tareas'))
        else:
            flash("Complete todos los campos")
            return redirect(url_for('rutas.tareas'))
    except Exception:
        exception("Error")
        return "Error Servidor"

    
@rutas.route('/tareas/eliminar_tarea/<int:id>')
def eliminar_tarea(id):
    try:
        tarea=Tarea.query.filter_by(id=id).first()
        db.session.delete(tarea)
        db.session.commit()
        flash("Tarea eliminada exitosamente")
        return redirect(url_for('rutas.tareas'))
    except Exception:
        exception("Error")
        return "Error Servidor"
    p
@rutas.route('/tareas/editar_tarea/<int:id>', methods=['POST', 'GET'])
def editar_tarea(id):
    try:
        tarea=Tarea.query.filter_by(id=id).first()
        if request.method=="GET":
            return render_template('/auth/editar_tarea.html', tarea=tarea)
        if request.method=="POST":
            print("Entre al post")
            tarea.titulo=request.form['titulo']
            tarea.descripcion=request.form['descripcion']
            if tarea.titulo=="" or tarea.descripcion=="":
                flash("Debe completar todos los campos")
                return render_template('/auth/editar_tarea.html', tarea=tarea)
            else:
                tarea.fecha=date.today()
                db.session.commit()
                flash("Tarea editada exitosamente")
                return redirect(url_for('rutas.tareas'))
    except Exception:
        exception("Error")
        return "Error servidor"
    


@rutas.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rutas.home'))
        

        
         
    
def status_401(error):
    return redirect(url_for('rutas.home'))

def status_404(error):
    return "<h1>La pagina no existe</h1>", 404
    


    



        
        
        




