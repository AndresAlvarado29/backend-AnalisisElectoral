from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db, candidato, red_social, consulta
from endpoints.reddit import buscarComentarios
from endpoints.youtube import buscar_videos
from endpoints.prediccionSentimientos import predecir_sentimiento

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

@app.route('/consultas', methods=['POST'])
def create_consulta():
    data = request.json
    nueva_consulta = consulta(
        nivel_aceptacion=data['nivel_aceptacion'],
        nivel_aceptacion_num=data['nivel_aceptacion_num'],
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

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
