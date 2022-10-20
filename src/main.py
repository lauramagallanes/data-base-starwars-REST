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
from models import db, People, Planet, User, Favorito
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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



# Creo el endpoint para people:

@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all() #esto obtiene todos los registros de personajes
    total_people = list(map(lambda item: item.serialize(), people))

    return jsonify(total_people), 200

# Creo el endpoint para planets:

@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all() #esto obtiene todos los registros de personajes
    total_planets = list(map(lambda item: item.serialize(), planets))

    return jsonify(total_planets), 200

# Creo el endpoint dinamico para people:

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    person = People.query.filter_by(id=people_id).first()

    return jsonify(person.serialize()), 200

# Creo el endpoint dinamico para planets:

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):

    planet = Planet.query.filter_by(id=planets_id).first()

    return jsonify(planet.serialize()), 200


# Creo el endpoint de user

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all() #esto obtiene todos los registros de usuarios
    total_users = list(map(lambda item: item.serialize(), users))

    return jsonify(total_users), 200

@app.route('/users', methods=['POST'])
def create_user():
    body = json.loads(request.data) #aca importo la info que viene del body desde el frontend
    

    query_user = User.query.filter_by(email=body["email"]).first() #aca consulto si el usuario que se queire crear ya existe
    
    if query_user is None:
        new_user = User(first_name=body["first_name"], last_name=body["last_name"], email=body["email"], password=body["password"], username=body["username"])
        db.session.add(new_user)
        db.session.commit()

        response_body = {
            "msg": "Created user"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "existed user"
        }
    return jsonify(response_body), 400

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>/favoritos', methods=['GET'])
def get_favorito(user_id):

    
    favorito = Favorito.query.filter_by(user_id=user_id).all()
    total_favoritos = list(map(lambda item: item.serialize(), favorito))

    return jsonify(total_favoritos), 200

# post para crear favoritos para un usuario x
@app.route('/users/<int:user_id>/favoritos/planet', methods=['POST'])
def create_favorito_planet(user_id):
    body = json.loads(request.data) #aca importo la info que viene del body desde el frontend
    
    query_favorito_planet = Favorito.query.filter_by(planet_id=body["planet_id"]).first() #aca consulto si el usuario ya tiene este planeta o personaje como favorito
    
    if query_favorito_planet is None:
        new_favorito_planet = Favorito(user_id=body["user_id"], planet_id=body["planet_id"], people_id=body["people_id"])
        db.session.add(new_favorito_planet)
        db.session.commit()

        response_body = {
            "msg": "Created user"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "existed favorite planet"
        }
    return jsonify(response_body), 400







 


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



