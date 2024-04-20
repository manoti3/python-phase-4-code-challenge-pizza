from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin # type: ignore

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizza = relationship('RestaurantPizza', back_populates='restaurant')
    pizza = association_proxy("restaurant_pizza", "pizza")


    # add serialization rules
    serialize_rules = ('-restaurant_pizza.restaurant',)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
    
    # add repr
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizza = relationship('RestaurantPizza', back_populates='pizza')
    restaurant = association_proxy("restaurant_pizza", "restaurant")


    # add serialization rules
    serialize_rules = ('-restaurant_pizza.pizza',)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id', ondelete='CASCADE'))

    restaurant = relationship('Restaurant', back_populates='restaurant_pizza')
    pizza = relationship('Pizza', back_populates='restaurant_pizza')


    # add serialization rules
    serialize_rules = ('-restaurant.restaurant_pizza', '-pizza.restaurant_pizza',)

    # add validation
    @validates('price')
    def validate_price(self, key, value):
        if value is None:
            raise ValueError("Price cannot be None")
        
        try:
            price = int(value)
        except ValueError:
            raise ValueError("Price must be an integer")

        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")

        return price
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"