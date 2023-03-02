# Create your models here.

from scenery_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)
    
class Landscape(FormEnum):
    DESERTS = 'Deserts'
    PLAINS = 'Plains'
    TAIGA = 'TAIGA'
    TUNDRA = 'Tundra'
    WETLAND = 'Wetland'
    MOUNTAINS = 'Mountain'
    CLIFFS = 'Cliffs'
    COAST = 'Coast'
    GLACIER = 'Glacier'
    SHRUBLAND = 'Shrubland'
    FOREST = 'Forest'
    RAINFOREST = 'Rain Forest'
    Woodland = 'Woodland'
    JUNGLE = 'Jungle'
    WATERFALL = 'Waterfall'
    OTHER = 'Other'

class Location(db.Model):
    """Location Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    visited_date = db.Column(db.Date)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', back_populates='locations')
    landscape = db.Column(db.Enum(Landscape), default=Landscape.DESERTS)
    entries = db.relationship(
        'Entry', secondary='location_entry', back_populates='locations'
    )
    users_who_favorited = db.relationship(
        'User', secondary='user_location', back_populates='favorite_locations'
    )

    def __str__(self):
        return f'<Location: {self.title}>'

    def __repr__(self):
        return f'<Location: {self.title}>'
    
class List(db.Model):
    """List model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500))
    locations = db.relationship('Location', back_populates='list')

    def __str__(self):
        return f'<List: {self.name}>'

    def __repr__(self):
        return f'<List: {self.name}>'
    
class Entry(db.Model):
    """Entry model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    locations = db.relationship(
        'Location', secondary='location_entry', back_populates='entries')

    def __str__(self):
        return f'<Entry: {self.name}>'

    def __repr__(self):
        return f'<Entry: {self.name}>'

location_entry_table = db.Table('location_entry',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_locations = db.relationship(
        'Location', secondary='user_location', back_populates='users_who_favorited')

    def __repr__(self):
        return f'<User: {self.username}>'

favorite_locations_table = db.Table('user_location',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)