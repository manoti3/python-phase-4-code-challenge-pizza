#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_dict = [restaurant.to_dict() for restaurant in restaurants]

        return jsonify(restaurant_dict)
    
class RestaurantByIdResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            pizzas = [
            {
                "id": restaurant_pizza.id,
                "pizza": {
                    "id": restaurant_pizza.pizza.id,
                    "name": restaurant_pizza.pizza.name,
                    "ingredients": restaurant_pizza.pizza.ingredients
                },
                "pizza_id": restaurant_pizza.pizza_id,
                "price": restaurant_pizza.price,
                "restaurant_id": restaurant_pizza.restaurant_id
            }
            for restaurant_pizza in restaurant.restaurant_pizza
        ]
            restaurant_dict['restaurant_pizzas'] = pizzas
            return jsonify(restaurant_dict)
        else:
            response_data = {"error": "Restaurant not found"}
            return make_response(jsonify(response_data), 404)    

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response_data = {"message": "Restaurant deleted"}
            return make_response(jsonify(response_data), 204)        
        else:
           response_data = {"error": "Restaurant not found"}
           return make_response(jsonify(response_data), 404)
        
class PizzaResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_dict = [pizza.to_dict() for pizza in pizzas]
        
        return jsonify(pizza_dict)
    
class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.json
        restaurant_id = data.get("restaurant_id")
        pizza_id = data.get("pizza_id")
        price = data.get("price")
        
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
        pizza = Pizza.query.filter_by(id=pizza_id).first()
        
        if price is None or not 1 <= price <= 30:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)
        
        restaurant_pizza = RestaurantPizza(restaurant_id=restaurant_id, pizza_id=pizza_id, price=price)
        db.session.add(restaurant_pizza)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        
        return make_response(jsonify({
            "id": restaurant_pizza.id,
            "pizza": pizza.to_dict(),
           "pizza_id": pizza_id,
            "price": price,
            "restaurant": restaurant.to_dict(),
            "restaurant_id": restaurant_id,
            }), 201)
        
api.add_resource(RestaurantResource, "/restaurants")
api.add_resource(RestaurantByIdResource, "/restaurants/<int:id>")
api.add_resource(PizzaResource, "/pizzas")
api.add_resource(RestaurantPizzaResource, "/restaurant_pizzas", methods=['POST'])

    
if __name__ == "__main__":
    app.run(port=5000, debug=True)