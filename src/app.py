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
from models import db, User, People, Planets, Favorite
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

@app.route('/people')
def get_people():
    try:
        characters = People.query.all()
        new_character_list = []
        for character in characters:
             new_character_list.append(character.serialize())
        if new_character_list:
            return jsonify(new_character_list), 200
        else:
            return jsonify({"msg", "Character no encontrado"}), 400
    except:
        return jsonify( {"msg": "Error Internal del Servidor"} ), 500
    
@app.route('/people/<int:people_id>')
def get_people_by_id(people_id):
    try:
        people = People.query.get(people_id)
        if people:
            return jsonify(people.serialize()), 200
        else:
            return jsonify({"msg", "Character no encontrado"}), 400
    except:
        return jsonify( {"msg": "Error Internal del Servidor"} ), 500
    
@app.route('/planets')
def get_planets():
    try:
        planets = Planets.query.all()
        new_planet_list = []
        for planet in planets:
            new_planet_list.append(planet.serialize())
        if new_planet_list:
            return jsonify(new_planet_list), 200
        else:
            return jsonify({"msg", "Planets no encontrado"}), 400
    except:
        return jsonify( {"msg": "Error Internal del Servidor"} ), 500
    
@app.route('/planets/<int:planet_id>')
def get_planets_by_id(planet_id):
    try:
        planet = Planets.query.get(planet_id)
        if planet:
            return jsonify(planet.serialize()), 200
        else:
            return jsonify({"msg", "Planets no encontrado"}), 400
    except:
        return jsonify( {"msg": "Error Internal del Servidor"} ), 500

@app.route('/users')
def get_user():
    try:
        users = User.query.all()
        new_user_list = []
        for user in users:
            new_user_list.append(user.serialize())
        return jsonify(new_user_list), 200
    except:
        return jsonify({"msg": "Error Internal Server"}), 500
    
@app.route('/users/favorites')
def get_users_favorite():
    try:
        user_id = request.args.get('user_id')
        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        get_favorite = [favorite.serialize() for favorite in user_favorites]
        print(user_id)
        print(user_favorites)
        print(get_favorite)
        return jsonify(get_favorite), 200

    except:
        return jsonify({"msg": "Error Internal Server"}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    try:
        user_id = request.args.get('user_id')
        favorites_people = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()

        if favorites_people:
            return jsonify({"msg":"Is a favorite people of the user"})

        people = People.query.get(people_id)
        if not people:
            return jsonify({"msg":"People does not exist"}), 400
        
        new_favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg":"People set a Favorite"}), 200
    except:
        return jsonify({"msg":"Error Internal Server"}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        user_id = request.args.get('user_id')
        favorites_planet = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if favorites_planet:
            return jsonify({"msg":"Is a favorite planet of the user"})

        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"msg":"planet does not exist"}), 400
        
        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg":"planet set a Favorite"}), 200
    except:
        return jsonify({"msg":"Error Internal Server"}), 500
    
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    try:
        user_id = request.args.get('user_id')
        favorite_to_delete = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()

        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            return jsonify({"msg":"Favorite People deleted"}), 200
        else:
            return jsonify({"msg":"Favorite People not found"}), 400
    except:
        return jsonify({"msg":"Error Internal Server"}), 500
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        user_id = request.args.get('user_id')
        favorite_to_delete = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
            return jsonify({"msg":"Favorite Planet deleted"}), 200
        else:
            return jsonify({"msg":"Favorite Planet not found"}), 400
    except:
        return jsonify({"msg":"Error Internal Server"}), 500
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
