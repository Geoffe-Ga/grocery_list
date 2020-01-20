from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.product import Product, ProductList
from resources.meal import Meal, MealList
from resources.transaction import Transaction, TransactionList
from resources.trip import Trip, TripList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dante'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Meal, '/meal/<string:name>')
api.add_resource(Product, '/product/<string:name>')
api.add_resource(Transaction, '/transaction/<int:id>')
api.add_resource(Trip, '/trip/<int:id>')

api.add_resource(MealList, '/meals')
api.add_resource(ProductList, '/products')
api.add_resource(TripList, '/trips')
api.add_resource(TransactionList, '/transactions')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
