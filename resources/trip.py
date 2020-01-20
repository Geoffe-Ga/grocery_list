from flask_restful import Resource
from models.trip import TripModel


class Trip(Resource):
    def get(self, trip_id):
        trip = TripModel.find_by_id(trip_id=trip_id)
        if trip:
            return trip.json()
        return {'message': 'Trip not found for the specified date'}, 404

    def post(self, date, cost):
        trip = TripModel.find_by_date_created(date=date)
        if not trip:
            trip = TripModel(0)
            try:
                trip.save_to_db()
            except:
                return {'message': 'An error occurred while creating the trip'}, 500
        else:
            try:
                trip.mark_done(cost)
            except:
                return {'message': 'An error occurred while completing the trip'}, 500

        return trip.json(), 201

    def delete(self, name):
        meal = MealModel.find_by_name(name)
        if meal:
            meal.delete_from_db()

        return {'message': 'Meal deleted'}


class TripList(Resource):
    def get(self):
        return {'trips': list(map(lambda x: x.json(), TripModel.query.all()))}
