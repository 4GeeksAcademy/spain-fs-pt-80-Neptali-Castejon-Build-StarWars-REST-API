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
from models import db, Users, People, Planets, Vehicles, Favorites
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


# Endpoint People

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
            return jsonify({"message": "People not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Endpoint Planets

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


# Endpoint para Eliminar persona favorita
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        request_body = request.json
        if not request_body or not isinstance(request_body, dict):
            return jsonify({"message": "Invalid or empty request body"}), 400

        user_id = request_body.get("user_id")
        if not user_id:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        favorite = Favorites.query.filter_by(user_id=user_id, favorite_id=people_id, favorite_type="people").first()
        if not favorite:
            return jsonify({"message": f"Favorite people with ID {people_id} not found for user {user_id}"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": f"Favorite people with ID {people_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    

# Endpoint para eliminar un planeta favorito con el id proporcionado
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        request_body = request.json
        if not request_body or not isinstance(request_body, dict):
            return jsonify({"message": "Invalid or empty request body"}), 400

        user_id = request_body.get("user_id")
        if not user_id:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        favorite = Favorites.query.filter_by(user_id=user_id, favorite_id=planet_id, favorite_type="planet").first()
        if not favorite:
            return jsonify({"message": f"Favorite planet with ID {planet_id} not found for user {user_id}"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": f"Favorite planet with ID {planet_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Endpoint para eliminar un vehicle favorito con el id proporcionado
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    try:
        request_body = request.json
        if not request_body or not isinstance(request_body, dict):
            return jsonify({"message": "Invalid or empty request body"}), 400

        user_id = request_body.get("user_id")
        if not user_id:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        favorite = Favorites.query.filter_by(user_id=user_id, favorite_id=vehicle_id, favorite_type="vehicle").first()
        if not favorite:
            return jsonify({"message": f"Favorite vehicle with ID {vehicle_id} not found for user {user_id}"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": f"Favorite vehicle with ID {vehicle_id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Endpoint Vehicles

# Endpoint para obtener todos los vehículos de la base de datos.
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()  # Consulta todos los registros de la tabla vehicles
    
    if not vehicles:  # Si no hay vehículos en la lista
        return jsonify({"msg": "No vehicles found"}), 404
    
    # Devuelve los datos serializados en JSON
    return jsonify([el.serialize() for el in vehicles]), 200


# Endpoint para recuperar un solo vehículo de la base de datos
@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_one_vehicle(vehicles_id):
    try:
        # Se busca al vehículo por su ID
        vehicle = Vehicles.query.get(vehicles_id)
        
        # Si se encuentra el vehículo, se devuelve como respuesta JSON
        if vehicle:
            return jsonify(vehicle.serialize()), 200
        else:
            return jsonify({"message": "Vehicle not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Endpoint Users

# Endpoint para obtener todas los usuarios de la base de datos.
@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()  # Consulta todos los registros de la tabla Users
    
    if not users:  # Si no hay usuarios en la lista
        return jsonify({"msg": "No users found"}), 404
    
    # Devuelve los datos serializados en JSON
    return jsonify([user.serialize() for user in users]), 200


# Endpoint para recuperar un solo usuario de la base de datos
@app.route('/users/<int:users_id>', methods=['GET'])
def get_user(users_id):
    try:
        # Se busca al usuario por su ID
        user = Users.query.get(users_id)
        
        # Si se encuentra el usuario, se devuelve como respuesta JSON
        if user:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Endpoint Favorites

# Endpoint para obtener todos los favoritos de un usuario
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        # Se busca al usuario por su ID
        user = Users.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # Se obtiene la lista de favoritos del usuario
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        
        if not favorites:
            return jsonify({"message": "No favorites found for this user"}), 404
        
        # Devuelve los favoritos serializados en JSON
        return jsonify([favorite.serialize() for favorite in favorites]), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

# Endpoint para añadir un nuevo favorito de tipo "people" al usuario actual
@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        request_body = request.json

        # Validar que el cuerpo de la solicitud no esté vacío
        if not request_body:
            return jsonify({"message": "Request body is empty"}), 400

        # Validar que los campos necesarios estén presentes
        if "user_id" not in request_body:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user_id = request_body["user_id"]

        # Validar que el usuario exista
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Validar que el planeta exista
        people = People.query.get(people_id)
        if not people:
            return jsonify({"message": "Planet not found"}), 404

        # Crear el nuevo favorito
        new_favorite = Favorites(user_id=user_id, favorite_id=people_id, favorite_type="people")

        # Guardar el favorito en la base de datos
        db.session.add(new_favorite)
        db.session.commit()

        # Respuesta exitosa
        return jsonify(new_favorite.serialize(), {"message": "People favorite added successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

# Endpoint para añadir un nuevo favorito de tipo "planet" al usuario actual
@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        request_body = request.json

        # Validar que el cuerpo de la solicitud no esté vacío
        if not request_body:
            return jsonify({"message": "Request body is empty"}), 400

        # Validar que los campos necesarios estén presentes
        if "user_id" not in request_body:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user_id = request_body["user_id"]

        # Validar que el usuario exista
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Validar que el planeta exista
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"message": "Planet not found"}), 404

        # Crear el nuevo favorito
        new_favorite = Favorites(user_id=user_id, favorite_id=planet_id, favorite_type="planet")

        # Guardar el favorito en la base de datos
        db.session.add(new_favorite)
        db.session.commit()

        # Respuesta exitosa
        return jsonify(new_favorite.serialize(), {"message": "Planet favorite added successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Endpoint para añadir un nuevo favorito de tipo "planet" al usuario actual
@app.route('/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    try:
        request_body = request.json

        # Validar que el cuerpo de la solicitud no esté vacío
        if not request_body:
            return jsonify({"message": "Request body is empty"}), 400

        # Validar que los campos necesarios estén presentes
        if "user_id" not in request_body:
            return jsonify({"message": "Missing required field: 'user_id'"}), 400

        user_id = request_body["user_id"]

        # Validar que el usuario exista
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Validar que el vehicle exista
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": "Vehicle not found"}), 404

        # Crear el nuevo favorito
        new_favorite = Favorites(user_id=user_id, favorite_id=vehicle_id, favorite_type="vehicle")

        # Guardar el favorito en la base de datos
        db.session.add(new_favorite)
        db.session.commit()

        # Respuesta exitosa
        return jsonify(new_favorite.serialize(), {"message": "Vehicle favorite added successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
