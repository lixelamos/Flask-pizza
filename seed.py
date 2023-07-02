from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)

# Import your models here
from models import Restaurant, Pizza, RestaurantPizza

# Define some test data
def create_test_data():
    # Create restaurants
    restaurant1 = Restaurant(name='Restaurant 1', address='Address 1')
    restaurant2 = Restaurant(name='Restaurant 2', address='Address 2')
    
    # Create pizzas
    pizza1 = Pizza(name='Pizza 1', ingredients='Ingredient 1, Ingredient 2')
    pizza2 = Pizza(name='Pizza 2', ingredients='Ingredient 3, Ingredient 4')
    
    # Create restaurant pizzas
    restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10)
    restaurant_pizza2 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=15)
    
    # Add the objects to the session
    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2, restaurant_pizza1, restaurant_pizza2])
    
    # Commit the session to persist the data in the database
    db.session.commit()

# Run the test data creation
if __name__ == '__main__':
    with app.app_context():
        create_test_data()
        print('Test data created successfully.')
