from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))

class red_social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))

class consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nivel_aceptacion = db.Column(db.String(200))
    nivel_aceptacion_num = db.Column(db.Float)
    fecha_consulta = db.Column(db.DateTime, default=datetime.utcnow)
    id_candidato= db.Column(db.Integer, db.ForeignKey('candidato.id'))
    id_red_social= db.Column(db.Integer, db.ForeignKey('red_social.id'))  
