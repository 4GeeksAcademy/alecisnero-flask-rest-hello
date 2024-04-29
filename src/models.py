from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)

    #campos
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    #Relations
    user = db.relationship('User', backref=db.backref('favorite', lazy=True))
    people = db.relationship('People', backref=db.backref('favorite', lazy=True))
    planet = db.relationship('Planets', backref=db.backref('favorite', lazy=True))


    """ people = db.relationship('People', back_populates='favorite', cascade='all, delete-orphan', single_parent=True)
    planets = db.relationship('Planets', back_populates='favorite', cascade='all, delete-orphan', single_parent=True) """
    """ favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.favorite_id'), nullable=False)
    people = db.relationship('Favorite', back_populates='people', single_parent=True, cascade='all, delete-orphan') """
    """ favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.favorite_id'), nullable=False)
    planets = db.relationship('Favorite', back_populates='planets', single_parent=True, cascade='all, delete-orphan') """

    def __repr__(self):
        return '<favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id ,
            "people_id": self.people_id ,
            "planet_id": self.planet_id ,
            # do not serialize the password, its a security breach
        }

    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False) 
    name = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    skin_color = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<people %r>' % self.id

    def serialize(self):
        return {
            "id": self.id ,
            "name": self.name ,
            "eye_color": self.eye_color ,
            "height": self.height ,
            "skin_color": self.skin_color ,
            "gender": self.gender ,
        }    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)
    orbital_period = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(120), unique=False, nullable=True)
    rotation_period = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return'<planets %r>' %self.id
    
    def serialize(self):
        return {
            "id": self.id ,
            "name": self.name ,
            "diameter": self.diameter ,
            "gravity": self.gravity ,
            "population": self.population ,
            "orbital_period": self.orbital_period ,
            "climate": self.climate ,
            "rotation_period": self.rotation_period ,
        }

