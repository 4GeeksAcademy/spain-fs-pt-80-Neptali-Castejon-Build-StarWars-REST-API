"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# Endpoint para obtener todas las personas de la base de datos.
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()  # Consulta todos los registros de la tabla People
    
    if not people:  # Si no hay usuarios en la lista
        return jsonify({"msg": "No people found"}), 404
    
    # Devuelve los datos serializados en JSON
    return jsonify([person.serialize() for person in people]), 200


# Endpoint para recuperar una sola persona de la base de datos
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    try:
        # Se busca a la persona por su ID
        person = People.query.get(people_id)
        
        # Si se encuentra la persona, se devuelve como respuesta JSON
        if person:
            return jsonify(person.serialize()), 200
        else:
            return jsonify({"message": "Member not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    
# Endpoint para obtener todos los planetas de la base de datos.
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()  # Consulta todos los registros de la tabla Planets
    
    if not planets:  # Si no hay planetas en la lista
        return jsonify({"msg": "No planets found"}), 404
    
    # Devuelve los datos serializados en JSON
    return jsonify([el.serialize() for el in planets]), 200


# Endpoint para recuperar una sola persona de la base de datos
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    try:
        # Se busca a la persona por su ID
        planets = Planets.query.get(planets_id)
        
        # Si se encuentra la persona, se devuelve como respuesta JSON
        if planets:
            return jsonify(planets.serialize()), 200
        else:
            return jsonify({"message": "Planets not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Endpoint para obtener todas los usuarios de la base de datos.
@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()  # Consulta todos los registros de la tabla Users
    
    if not users:  # Si no hay usuarios en la lista
        return jsonify({"msg": "No users found"}), 404
    
    # Devuelve los datos serializados en JSON
    return jsonify([user.serialize() for user in users]), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
