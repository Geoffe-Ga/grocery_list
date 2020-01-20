from db import db
from datetime import datetime


class TripModel(db.Model):
    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True)

    cost = db.Column(db.Integer)

    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow())
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.utcnow())
    completed_at = db.Column('completed_at', db.DateTime)

    def __init__(self, cost):
        self.cost = cost

    def json(self):
        return {'created_at': self.created_at, 'completed_at': self.completed_at, 'cost': self.cost}

    @classmethod
    def find_by_date_created(cls, date):
        return cls.query.filter_by(created_at=date).all()

    @classmethod
    def find_by_id(cls, trip_id):
        return cls.query.filter_by(id=trip_id)

    def mark_done(self, cost):
        self.completed_at = datetime.utcnow()
        self.cost = cost
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()