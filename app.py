from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Route handler for GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    from models import Restaurant  # Import here to avoid circular import
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in restaurants]
    return jsonify(restaurant_list)


# Route handler for GET /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    from models import Restaurant  # Import here to avoid circular import
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    restaurant_data = {'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}
    return jsonify(restaurant_data)


# Route handler for DELETE /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    from models import Restaurant, RestaurantPizza  # Import here to avoid circular import
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204


# Route handler for GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    from models import Pizza  # Import here to avoid circular import
    pizzas = Pizza.query.all()
    pizza_list = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas]
    return jsonify(pizza_list)


# Route handler for GET /pizzas/:id

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    from models import Pizza, Restaurant, RestaurantPizza  # Import here to avoid circular import
    data = request.json
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not pizza_id or not restaurant_id:
        return jsonify({'errors': ['validation errors']}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'errors': ['validation errors']}), 400

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    pizza_data = {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
    return jsonify(pizza_data), 201

if __name__ == '__main__':
    app.run(port=5555)
