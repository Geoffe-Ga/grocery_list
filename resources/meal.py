from flask_restful import Resource
from models.meal import MealModel


class Meal(Resource):
    def get(self, name):
        meal = MealModel.find_by_name(name)
        if meal:
            return meal.json()
        return {'message': 'Meal not found'}, 404

    def post(self, name):
        if MealModel.find_by_name(name):
            return {'message': "Meal '{}' already exists".format(name)}, 400

        meal = MealModel(name)
        try:
            meal.save_to_db()
        except:
            return {'message': 'An error occurred while creating the meal'}, 500

        return meal.json(), 201

    def delete(self, name):
        meal = MealModel.find_by_name(name)
        if meal:
            meal.delete_from_db()

        return {'message': 'Meal deleted'}


class MealList(Resource):
    def get(self):
        return {'meals': list(map(lambda x: x.json(), MealModel.query.all()))}
