from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db, candidato, red_social, consulta
from endpoints.reddit import buscarComentarios
from endpoints.youtube import obtener_solo_comentarios
from endpoints.prediccionSentimientos import predecir_sentimiento, predict_sentiment
from endpoints.facebook import obtener_solo_comentarios_facebook
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../database/scrapEE.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)
ma= Marshmallow(app)

def analizar_sentimientos(comentarios):
    if not comentarios:
        return {"error": "No se encontraron comentarios para analizar."}

    # Predecir los sentimientos
    resultados = [{"comentario": c, "sentimiento": predict_sentiment(c)} for c in comentarios]

    # Inicializar el conteo de sentimientos
    conteo = {"Muy Positivo": 0, "Positivo": 0, "Neutro": 0, "Negativo": 0, "Muy Negativo": 0}

    # Contar ocurrencias de cada sentimiento
    for r in resultados:
        conteo[r["sentimiento"]] += 1

    total_comentarios = sum(conteo.values())
    nivel_aceptacion = ((conteo["Muy Positivo"] + conteo["Positivo"]) / total_comentarios * 100) if total_comentarios > 0 else 0

    # Definir el nivel de aceptación
    if nivel_aceptacion >= 60:
        nivel = "Alto"
    elif nivel_aceptacion >= 30:
        nivel = "Medio"
    else:
        nivel = "Bajo"

    return {
        "comentarios": resultados,
        "total_comentarios": total_comentarios,
        "conteo": conteo,
        "nivel_aceptacion": nivel_aceptacion,
        "clasificacion_nivel": nivel
    }

class CandidatoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = candidato

class RedSocialSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = red_social

class ConsultaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = consulta

candidato_schema = CandidatoSchema()
candidatos_schema = CandidatoSchema(many=True)
red_social_schema = RedSocialSchema()
redes_sociales_schema = RedSocialSchema(many=True)
consulta_schema = ConsultaSchema()
consultas_schema = ConsultaSchema(many=True)

# CRUD
@app.route('/candidatos', methods=['POST'])
def create_candidato():
    nombre = request.json['nombre']
    nuevo_candidato = candidato(nombre=nombre)
    db.session.add(nuevo_candidato)
    db.session.commit()
    return candidato_schema.jsonify(nuevo_candidato)

@app.route('/candidatos', methods=['GET'])
def get_candidatos():
    candidatos = candidato.query.all()
    return jsonify(candidatos_schema.dump(candidatos))

@app.route('/candidatos/<int:id>', methods=['DELETE'])
def delete_candidato(id):
    candidato = candidato.query.get(id)
    if candidato:
        db.session.delete(candidato)
        db.session.commit()
        return jsonify({'message': 'candidato eliminado'})
    return jsonify({'message': 'candidato no encontrado'}), 404

@app.route('/candidatos/<int:id>', methods=['GET'])
def get_candidato_by_id(id):
    candidato = candidato.query.get(id)
    if not candidato:
        return jsonify({'error': 'Candidato no encontrado'}), 404
    return candidato_schema.jsonify(candidato)

@app.route('/candidatos/nombre/<string:nombre>', methods=['GET'])
def get_candidato_by_nombre(nombre):
    candidato = candidato.query.filter_by(nombre=nombre).first()
    if not candidato:
        return jsonify({'error': 'Candidato no encontrado'}), 404
    return candidato_schema.jsonify(candidato)
@app.route('/redes_sociales', methods=['POST'])
def create_red_social():
    nombre = request.json['nombre']
    nueva_red = red_social(nombre=nombre)
    db.session.add(nueva_red)
    db.session.commit()
    return red_social_schema.jsonify(nueva_red)

@app.route('/redes_sociales', methods=['GET'])
def get_redes_sociales():
    redes = red_social.query.all()
    return jsonify(redes_sociales_schema.dump(redes))
@app.route('/redes_sociales/<int:id>', methods=['GET'])
def get_red_social_by_id(id):
    red = red_social.query.get(id)
    if not red:
        return jsonify({'error': 'Red social no encontrada'}), 404
    return red_social_schema.jsonify(red)

@app.route('/redes_sociales/nombre/<string:nombre>', methods=['GET'])
def get_red_social_by_nombre(nombre):
    red = red_social.query.filter_by(nombre=nombre).first()
    if not red:
        return jsonify({'error': 'Red social no encontrada'}), 404
    return red_social_schema.jsonify(red)

@app.route('/consultas', methods=['POST'])
def create_consulta():
    data = request.json
    nueva_consulta = consulta(
        nivel_aceptacion=data['nivel_aceptacion'],
        nivel_aceptacion_num=data['nivel_aceptacion_num'],
        numero_comentarios=data['numero_comentarios'],
        id_candidato=data['id_candidato'],
        id_red_social=data['id_red_social']
    )
    db.session.add(nueva_consulta)
    db.session.commit()
    return consulta_schema.jsonify(nueva_consulta)

@app.route('/consultas', methods=['GET'])
def get_consultas():
    consultas = consulta.query.all()
    return jsonify(consultas_schema.dump(consultas))

@app.route('/consultas/<int:id>', methods=['DELETE'])
def delete_consulta(id):
    consulta = consulta.query.get(id)
    if consulta:
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({'message': 'consulta eliminada'})
    return jsonify({'message': 'consulta no encontrada'}), 404
#CONSULTAS API

# Lista de candidatos
CANDIDATOS = [
    {"id": 1, "nombre": "Jimmy Jairala"},
    {"id": 2, "nombre": "Jorge Escala"},
    {"id": 3, "nombre": "Andrea Gonzalez"},
    {"id": 4, "nombre": "Victor Araus"},
    {"id": 5, "nombre": "Luisa Gonzalez"},
    {"id": 6, "nombre": "Henry Kronfle"},
    {"id": 7, "nombre": "Daniel Noboa"},
    {"id": 8, "nombre": "Luis F. Tilleria"},
    {"id": 9, "nombre": "Carlos Rabascall"},
    {"id": 10, "nombre": "Juan I. Cueva"},
    {"id": 11, "nombre": "Pedro Granja"},
    {"id": 12, "nombre": "Leonidas Iza"},
    {"id": 13, "nombre": "Ivan Saquicela"},
    {"id": 14, "nombre": "Francesco Tabacchi"},
    {"id": 15, "nombre": "Wilson Gomez"},
    {"id": 16, "nombre": "Henry Cucalon"},
]

# Lista de redes sociales
REDES_SOCIALES = {
    "Facebook": 1,
    "Youtube": 2,
    "Reddit": 3
}

def analizar_sentimientos_y_guardar(comentarios, query, red_social):
    """
    Analiza sentimientos, obtiene nivel de aceptación y guarda la consulta en la base de datos.
    """
    if not comentarios:
        return {"error": "No se encontraron comentarios para analizar."}

    # Predecir los sentimientos
    resultados = [{"comentario": c, "sentimiento": predict_sentiment(c)} for c in comentarios]

    # Inicializar el conteo de sentimientos
    conteo = {"Muy Positivo": 0, "Positivo": 0, "Neutro": 0, "Negativo": 0, "Muy Negativo": 0}

    # Contar ocurrencias de cada sentimiento
    for r in resultados:
        conteo[r["sentimiento"]] += 1

    total_comentarios = sum(conteo.values())
    nivel_aceptacion = ((conteo["Muy Positivo"] + conteo["Positivo"]) / total_comentarios * 100) if total_comentarios > 0 else 0

    # Definir el nivel de aceptación
    if nivel_aceptacion >= 60:
        nivel = "Alto"
    elif nivel_aceptacion >= 30:
        nivel = "Medio"
    else:
        nivel = "Bajo"

    # Identificar si el nombre de un candidato está en la búsqueda
    id_candidato = None
    for candidato in CANDIDATOS:
        if candidato["nombre"].lower() in query.lower():
            id_candidato = candidato["id"]
            break

    # Guardar en la base de datos
    nueva_consulta = consulta(
        nivel_aceptacion=nivel,
        nivel_aceptacion_num=nivel_aceptacion,
        numero_comentarios=total_comentarios,
        id_candidato=id_candidato,
        id_red_social=REDES_SOCIALES.get(red_social, None)  # Si no coincide, será None
    )
    db.session.add(nueva_consulta)
    db.session.commit()

    return {
        "comentarios": resultados,
        "total_comentarios": total_comentarios,
        "conteo": conteo,
        "nivel_aceptacion": nivel_aceptacion,
        "clasificacion_nivel": nivel
    }

@app.route('/api/buscar_facebook', methods=['POST'])
def buscar_facebook_y_predecir():
    """
    Endpoint que obtiene comentarios de Facebook, analiza sentimientos y guarda en la base de datos.
    """
    data = request.json
    palabra_clave = data.get("query")

    if not palabra_clave:
        return jsonify({"error": "Se requiere una palabra clave para buscar publicaciones."}), 400
    
    comentarios = obtener_solo_comentarios_facebook(palabra_clave)
    return jsonify(analizar_sentimientos_y_guardar(comentarios.get("comentarios", []), palabra_clave, "Facebook"))

@app.route('/api/buscar_reddit', methods=['POST'])
def buscar_reddit_y_predecir():
    """
    Endpoint que obtiene comentarios de Reddit, analiza sentimientos y guarda en la base de datos.
    """
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Se requiere un parámetro de búsqueda"}), 400

    comentarios = buscarComentarios(query)
    return jsonify(analizar_sentimientos_y_guardar(comentarios.get("comentarios", []), query, "Reddit"))

@app.route('/api/buscar_youtube', methods=['POST'])
def buscar_youtube_y_predecir():
    """
    Endpoint que obtiene comentarios de YouTube, analiza sentimientos y guarda en la base de datos.
    """
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Se requiere un parámetro de búsqueda"}), 400

    comentarios = obtener_solo_comentarios(query)
    return jsonify(analizar_sentimientos_y_guardar(comentarios.get("comentarios", []), query, "Youtube"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)