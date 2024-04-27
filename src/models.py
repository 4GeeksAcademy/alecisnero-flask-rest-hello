from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False) 
    last_name = db.Column(db.String(120), unique=False, nullable=False) 

    def __repr__(self):
        return '<user %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True, nullable=False) 
    people_id = db.Column(db.Integer, db.ForeignKey('favorite.id'), nullable=False)
    people_rel= db.relationship('Favorite')
    name = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    skin_color = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)

    def __ref__(self):
        return '<people %r>' % self.id

    def serialize(self):
        return {
            "id": self.id ,
            "people_id": self.people_id,
            "name": self.name ,
            "eye_color": self.eye_color ,
            "height": self.height ,
            "skin_color": self.skin_color ,
            "gender": self.gender ,
        }    

class Planets(db.Model):
    __tablename__ = 'plantes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    planets_rel = db.relationship('Favorite')
    name = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)
    orbital_period = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(120), unique=False, nullable=True)
    rotation_period = db.Column(db.Integer, unique=False, nullable=True)

    def __ref__(self):
        return'<plantes %r>' %self.id
    
    def serialize(self):
        return {
            "id": self.id ,
            "planets_id": self.planets_id,
            "name": self.name ,
            "diameter": self.diameter ,
            "gravity": self.gravity ,
            "population": self.population ,
            "orbital_period": self.orbital_period ,
            "climate": self.climate ,
            "rotation_period": self.rotation_period ,
        }