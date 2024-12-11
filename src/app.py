import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, People, Planet, Favorite
from utils import APIException, generate_sitemap
from admin import setup_admin
    
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
    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return jsonify(error.to_dict()), error.status_code
    @app.route('/')
    def sitemap():
        return generate_sitemap(app)
    @app.route('/people', methods=['GET'])
    def get_all_people():
        people = People.query.all()
        return jsonify([person.serialize() for person in people]), 200
    @app.route('/people/<int:people_id>', methods=['GET'])
    def get_person(people_id):
        person = People.query.get(people_id)
        if person is None:
            raise APIException("Person not found", 404)
        return jsonify(person.serialize()), 200
    @app.route('/planets', methods=['GET'])
    def get_all_planets():
        planets = Planet.query.all()
        return jsonify([planet.serialize() for planet in planets]), 200
    @app.route('/planets/<int:planet_id>', methods=['GET'])
    def get_planet(planet_id):
        planet = Planet.query.get(planet_id)
        if planet is None:
            raise APIException("Planet not found", 404)
        return jsonify(planet.serialize()), 200
    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    @app.route('/users/favorites', methods=['GET'])
    def get_user_favorites():
        user_id = request.args.get('user_id')
        user = User.query.get(user_id)
        if user is None:
            raise APIException("User not found", 404)
        return jsonify([favorite.serialize() for favorite in user.favorites]), 200
    @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
    def add_favorite_planet(planet_id):
        user_id = request.json.get('user_id')
        user = User.query.get(user_id)
        planet = Planet.query.get(planet_id)
        if not user or not planet:
            raise APIException("User or Planet not found", 404)
        favorite = Favorite(user_id=user.id, planet_id=planet.id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    @app.route('/favorite/people/<int:people_id>', methods=['POST'])
    def add_favorite_person(people_id):
        user_id = request.json.get('user_id')
        user = User.query.get(user_id)
        person = People.query.get(people_id)
        if not user or not person:
            raise APIException("User or Person not found", 404)
        favorite = Favorite(user_id=user.id, people_id=person.id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    @app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
    def remove_favorite_planet(planet_id):
        user_id = request.args.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            raise APIException("Favorite not found", 404)
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite removed"}), 200
    @app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
    def remove_favorite_person(people_id):
        user_id = request.args.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if not favorite:
            raise APIException("Favorite not found", 404)
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite removed"}), 200
    if __name__ == '__main__':
        PORT = int(os.environ.get('PORT', 3000))
        app.run(host='0.0.0.0', port=PORT, debug=True)