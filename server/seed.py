#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")

    # Define pizza names and ingredients
    pizzas_data = [
        ("Margherita", "Tomato sauce, mozzarella, basil"),
        ("Pepperoni", "Tomato sauce, mozzarella, pepperoni"),
        ("Hawaiian", "Tomato sauce, mozzarella, ham, pineapple"),
        ("BBQ Chicken", "BBQ sauce, mozzarella, chicken, onions"),
        ("Vegetarian", "Tomato sauce, mozzarella, mushrooms, peppers, onions"),
        ("Meat Lovers", "Tomato sauce, mozzarella, pepperoni, sausage, bacon"),
        ("Supreme", "Tomato sauce, mozzarella, pepperoni, sausage, mushrooms, peppers, onions"),
        ("Buffalo Chicken", "Buffalo sauce, mozzarella, chicken, red onions, ranch drizzle"),
        ("Margarita", "Tomato sauce, mozzarella, basil, olive oil"),
        ("Pesto Chicken", "Pesto sauce, mozzarella, chicken, tomatoes, spinach"),
    ]

    # Create pizzas for each restaurant
    pizzas = []
    for restaurant in restaurants:
        for pizza_name, pizza_ingredients in pizzas_data:
            pizza = Pizza(name=pizza_name, ingredients=pizza_ingredients)
            pizzas.append(pizza)
            db.session.add(pizza)

    print("Creating RestaurantPizza...")

    # Create RestaurantPizza entries
    restaurantPizzas = []
    for i, restaurant in enumerate(restaurants):
        for j in range(len(pizzas_data)):
            price = (i + 1) * (j + 1)  # Price based on restaurant and pizza index
            rp = RestaurantPizza(restaurant=restaurant, pizza=pizzas[i * len(pizzas_data) + j], price=price)
            restaurantPizzas.append(rp)
            db.session.add(rp)

    db.session.commit()

    print("Seeding done!")