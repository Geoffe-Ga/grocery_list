from db import db
from datetime import datetime


class MealModel(db.Model):
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    products = db.relationship('ProductModel', lazy='dynamic')  # if lazy='dynamic', products is a query builder

    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.utcnow())

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'products': list(map(lambda x: x.json(), self.products.all()))}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
