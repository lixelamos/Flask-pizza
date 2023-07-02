from app import db
from datetime import datetime
from sqlalchemy.orm import validates

class Pizza(db.Model):
    __tablename__ = 'pizza'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self):
        return f'Pizza(id={self.id}, name={self.name}, ingredients={self.ingredients})'

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref='restaurants')
    
    def __str__(self):
        return f'Restaurant(id={self.id}, name={self.name}, address={self.address})'

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError('Price must be between 1 and 30')
        return price
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))
    pizza = db.relationship('Pizza', backref=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))
    
    def __str__(self):
        return f'RestaurantPizza(id={self.id}, restaurant_id={self.restaurant_id}, pizza_id={self.pizza_id}, price={self.price})'
