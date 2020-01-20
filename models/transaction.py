from db import db
from datetime import datetime


class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('ProductModel')

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    trip = db.relationship('TripModel')

    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.utcnow())
    completed_at = db.Column('completed_at', db.DateTime)

    def __init__(self, trip_id, product_id):
        self.trip_id = trip_id
        self.product_id = product_id

    def json(self):
        return {'id': self.id,
                'created_at': self.created_at,
                'completed_at': self.completed_at,
                'product': self.product.name,
                'trip': self.trip.id}

    @classmethod
    def find_unfinished(cls, product_id):
        return cls.query.filter_by(product_id=product_id, completed_at=None).first()

    @classmethod
    def find_by_id(cls, trans_id):
        return cls.query.filter_by(id=trans_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def mark_done(self):
        self.completed_at = datetime.utcnow()
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()