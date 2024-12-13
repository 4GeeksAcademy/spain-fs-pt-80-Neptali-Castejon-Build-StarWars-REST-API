from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)  # ID del favorito
    favorite_type = db.Column(db.String(50), nullable=False)  # Tipo (e.g., "people", "planets", "vehicles")
    extra_info = db.Column(db.Text)

    user = db.relationship('Users', backref='favorites')
    
    def __repr__(self):
        return f'<Favorites {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_id": self.favorite_id,
            "favorite_type": self.favorite_type,
            "extra_info": self.extra_info,
        }

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "user_id": self.user_id,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    orbital_period = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    rotation_period = db.Column(db.String(50), nullable=False)
    surface_water = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Planets {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cargo_capacity = db.Column(db.String(100), nullable=False)
    consumables = db.Column(db.String(100), nullable=False)
    cost_in_credits = db.Column(db.String(100), nullable=False)
    crew = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    max_atmosphering_speed = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    passengers = db.Column(db.String(100), nullable=False)
    vehicle_class = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Vehicles {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "length": self.length,
            "manufacturer": self.manufacturer,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "model": self.model,
            "passengers": self.passengers,
            "vehicle_class": self.vehicle_class,
        }
