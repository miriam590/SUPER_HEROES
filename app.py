# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, Hero_Power

# Fix the error here by using __name__ instead of _name_
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Home route
@app.route('/')
def home():
    return jsonify("Welcome to my SuperHero API!")

# Get all heroes
@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(only=("id", "name", "super_name")) for hero in heroes]), 200

# Get hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = hero.to_dict()
    hero_data["hero_powers"] = [
        {
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": hp.power.to_dict(only=("id", "name", "description"))
        } for hp in hero.hero_powers
    ]
    return jsonify(hero_data), 200

# Delete a hero by ID
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"errors": ["Hero not found"]}), 404
    db.session.delete(hero)
    db.session.commit()
    return jsonify({"message": "Hero deleted successfully"}), 200

# Get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict(only=("id", "name", "description")) for power in powers]), 200

# Update a power
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if "description" in data and len(data["description"]) >= 20:
        power.description = data["description"]
        db.session.commit()
        return jsonify(power.to_dict(only=("id", "name", "description"))), 200
    else:
        return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400

# Create a hero power
@app.route('/heropowers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero = Hero.query.get(data.get("hero_id"))
    power = Power.query.get(data.get("power_id"))
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 404

    if data.get("strength") not in ["Strong", "Weak", "Average"]:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 400

    hero_power = Hero_Power(
        hero_id=data["hero_id"],
        power_id=data["power_id"],
        strength=data["strength"]
    )

    db.session.add(hero_power)
    db.session.commit()

    response_data = hero_power.to_dict()
    response_data["hero"] = hero.to_dict(only=("id", "name", "super_name"))
    response_data["power"] = power.to_dict(only=("id", "name", "description"))

    return jsonify(response_data), 201

if __name__ == '__main__':
    app.run(debug=True)

