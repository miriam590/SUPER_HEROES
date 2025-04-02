from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):  
    __tablename__ = "heroes"  # Corrected to __tablename__
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    serialize_rules = ('-hero_powers.hero',)

    # relationship (a hero has many hero_powers)
    hero_powers = db.relationship("Hero_Power", back_populates="hero", cascade="all, delete")

class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"  # Corrected to __tablename__
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)

    serialize_rules = ('-hero_powers.power',)
    # relationship (a power has many hero_powers)
    hero_powers = db.relationship("Hero_Power", back_populates="power", cascade="all, delete")
    
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

class Hero_Power(db.Model, SerializerMixin):
    __tablename__ = "heropowers"  # Corrected to __tablename__
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, ForeignKey('powers.id'))
    strength = db.Column(db.String, nullable=False)

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # relationships
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")

    # a hero can only have a power once
    __table_args__ = (UniqueConstraint('hero_id', 'power_id', name='unique_hero_power'),)

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ["Strong", "Weak", "Average"]:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return value
