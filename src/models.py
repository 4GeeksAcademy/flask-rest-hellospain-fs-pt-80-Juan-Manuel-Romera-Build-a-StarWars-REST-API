from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
                                
    def serialize(self):
        return {"id": self.id, "email": self.email}

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    birth_year = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.String(10), nullable=True)

    def serialize(self):
        return {"id": self.id, "name": self.name, "birth_year": self.birth_year, "gender": self.gender}
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {"id": self.id, "name": self.name, "climate": self.climate, "terrain": self.terrain}
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "people_id": self.people_id, "planet_id": self.planet_id}
    
