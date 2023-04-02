from flask import Flask
from dotenv import load_dotenv
import os
from routes.rutas import rutas, status_401, status_404
from config import config

load_dotenv()



app=Flask(__name__)

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI']=f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config.from_object(config['development'])
app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)

app.register_blueprint(rutas)
