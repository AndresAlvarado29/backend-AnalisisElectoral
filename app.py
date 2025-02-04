from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db, candidato, red_social, consulta
from endpoints.reddit import buscarComentarios
from endpoints.youtube import buscar_videos
from endpoints.prediccionSentimientos import predecir_sentimiento, predict_sentiment
from endpoints.facebook import obtener_comentarios_facebook 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../database/scrapEE.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)
ma= Marshmallow(app)

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
@app.route('/api/facebook_comments', methods=['POST'])
def obtener_comentarios():
    data = request.json
    palabra_clave = data.get("query")
    if not palabra_clave:
        return jsonify({"error": "Se requiere una palabra clave para buscar publicaciones."}), 400
    
    comentarios = obtener_comentarios_facebook(palabra_clave)
    return jsonify({"comentarios": comentarios})

@app.route('/api/buscar_reddit', methods=['GET'] )
def buscar_Reddit():
    query = request.args.get('query','')
    if not query:
        return jsonify({"error":"Se requiere un parámetro de búsqueda"}), 400
    resultado = buscarComentarios(query)
    return jsonify(resultado)

@app.route('/api/buscar_youtube', methods=['GET'])
def buscar_Youtube():
    query = request.args.get('query','')
    if not query:
        return jsonify({"error":"Se requiere un parámetro de búsqueda"}), 400
    resultado = buscar_videos(query)
    return jsonify(resultado)
#prediccion con el modelo
@app.route('/api/predecir_sentimiento', methods=['POST'])
def predecir_sentimiento_api():
    data = request.json
    comentarios = data.get('comentarios', [])
    
    if not comentarios:
        return jsonify({"error": "Se requiere una lista de comentarios"}), 400
    
    resultados = [predecir_sentimiento(comentario) for comentario in comentarios]
    conteo = {"Positivo": 0, "Neutro": 0, "Negativo": 0}
    
    for resultado in resultados:
        conteo[resultado] += 1
    
    total = sum(conteo.values())
    nivel_aceptacion = (conteo["Positivo"] / total) * 100 if total > 0 else 0
    
    if nivel_aceptacion >= 60:
        nivel = "Alto"
    elif nivel_aceptacion >= 30:
        nivel = "Medio"
    else:
        nivel = "Bajo"
    
    return jsonify({
        "resultados": resultados,
        "conteo": conteo,
        "nivel_aceptacion": nivel_aceptacion,
        "clasificacion_nivel": nivel
    })
@app.route('/api/predecir_sentimiento2', methods=['POST'])
def predecir_sentimiento_api2():
    data = request.json
    comentarios = data.get('comentarios', [])

    if not comentarios:
        return jsonify({"error": "Se requiere una lista de comentarios"}), 400

    resultados = [predict_sentiment(comentario) for comentario in comentarios]
    
    # Inicializar el conteo de cada sentimiento
    conteo = {"Muy Positivo": 0, "Positivo": 0, "Neutro": 0, "Negativo": 0, "Muy Negativo": 0}

    # Contar ocurrencias de cada sentimiento
    for sentimiento in resultados:
        conteo[sentimiento] += 1  # Ahora 'sentimiento' es un string y sí puede ser clave en el diccionario

    total = sum(conteo.values())
    nivel_aceptacion = (conteo["Positivo"] / total) * 100 if total > 0 else 0

    # Definir el nivel de aceptación
    if nivel_aceptacion >= 60:
        nivel = "Alto"
    elif nivel_aceptacion >= 30:
        nivel = "Medio"
    else:
        nivel = "Bajo"

    return jsonify({
        "resultados": resultados,
        "conteo": conteo,
        "nivel_aceptacion": nivel_aceptacion,
        "clasificacion_nivel": nivel
    })
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
