from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.transaction import TransactionModel


class Transaction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=int,
                        required=True,
                        help="Every transaction needs a product_id"
                        )

    parser.add_argument('trip_id',
                        type=int,
                        required=True,
                        help="Every transaction needs a trip_id"
                        )

    def get(self, trans_id):
        transaction = TransactionModel.find_by_id(trans_id)
        if transaction:
            return transaction.json()
        return {'message': 'Transaction not found'}, 404

    @jwt_required()
    def post(self, product_id):
        transaction = TransactionModel.find_unfinished(product_id=product_id)
        if transaction:
            try:
                transaction.mark_done()
            except:
                return {'message': 'An error occurred marking the transaction complete.'}, 500
        else:
            transaction = TransactionModel(product_id, trip_id=trip_id)

            try:
                transaction.save_to_db()
            except:
                return {'message': 'An error occurred writing to the transaction table.'}, 500

        return transaction.json(), 201

    @jwt_required()
    def delete(self, name):
        transaction = TransactionModel.find_by_id(name)
        if transaction:
            transaction.delete_from_db()

        return {'message': 'Transaction deleted'}


class TransactionList(Resource):
    def get(self):
        return {'trips': list(map(lambda x: x.json(), TransactionModel.query.all()))}
