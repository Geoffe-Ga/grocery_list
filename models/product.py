from db import db
from datetime import datetime


class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    meal = db.relationship('MealModel')

    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, name, meal_id):
        self.name = name
        self.meal_id = meal_id

    def json(self):
        return {'name': self.name, 'meal': self.meal.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
