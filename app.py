from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

api = Api(app)

migrate = Migrate(app, db)

db.init_app(app)


class Home(Resource):
    def get(self):
        return {"name": "Flask API"}


class RestaurantResource(Resource):
    def get(self, id=None):
        if id is None:
            return self.get_all()
        else:
            return self.get_by_id(id)

    def get_by_id(self, id):
        restaurant = db.session.query(Restaurant).filter_by(id=id).first()

        if restaurant:
            restaurant_obj = {
                'name': restaurant.name,
                'address': restaurant.address
            }
            response = make_response(jsonify(restaurant_obj), 200)
        else:
            response = make_response(jsonify({'error': 'Restaurant not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def get_all(self):
        restaurants = db.session.query(Restaurant).all()
        restaurant_list = [{
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        } for restaurant in restaurants]
        response = make_response(jsonify(restaurant_list), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    def post(self):
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')

        if name and address:
            restaurant = Restaurant(name=name, address=address)
            db.session.add(restaurant)
            db.session.commit()

            response = make_response(jsonify({'message': 'Restaurant created successfully'}), 201)
        else:
            response = make_response(jsonify({'error': 'Missing required fields'}), 400)

        response.headers['Content-Type'] = 'application/json'
        return response

    def put(self, id):
        restaurant = db.session.query(Restaurant).filter_by(id=id).first()

        if restaurant:
            data = request.get_json()
            name = data.get('name')
            address = data.get('address')

            if name and address:
                restaurant.name = name
                restaurant.address = address
                db.session.commit()
                message = {'message': 'Restaurant updated successfully'}
                status_code = 200
            else:
                message = {'error': 'Missing required fields'}
                status_code = 400
        else:
            message = {'error': 'Restaurant not found'}
            status_code = 404

        response = make_response(jsonify(message), status_code)
        response.headers['Content-Type'] = 'application/json'
        return response

    def delete(self, id):
        restaurant = db.session.query(Restaurant).filter_by(id=id).first()

        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response = make_response(jsonify({'message': 'Restaurant deleted successfully'}), 200)
        else:
            response = make_response(jsonify({'error': 'Restaurant not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response


class PizzaResource(Resource):
    def get(self, id=None):
        if id is None:
            return self.get_all()
        else:
            return self.get_by_id(id)

    def get_by_id(self, id):
        pizza = db.session.query(Pizza).filter_by(id=id).first()

        if pizza:
            pizza_obj = {
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }
            response = make_response(jsonify(pizza_obj), 200)
        else:
            response = make_response(jsonify({'error': 'Pizza not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def get_all(self):
        pizzas = db.session.query(Pizza).all()
        pizza_list = []
        for pizza in pizzas:
            pizza_obj = {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }
            pizza_list.append(pizza_obj)
        response = make_response(jsonify(pizza_list), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    def post(self):
        data = request.get_json()
        name = data.get('name')
        ingredients = data.get('ingredients')

        if name and ingredients:
            pizza = Pizza(name=name, ingredients=ingredients)
            db.session.add(pizza)
            db.session.commit()

            response = make_response(jsonify({'message': 'Pizza created successfully'}), 201)
        else:
            response = make_response(jsonify({'error': 'Missing required fields'}), 400)

        response.headers['Content-Type'] = 'application/json'
        return response

    def put(self, id):
        pizza = db.session.query(Pizza).filter_by(id=id).first()

        if pizza:
            data = request.get_json()
            name = data.get('name')
            ingredients = data.get('ingredients')

            if name and ingredients:
                pizza.name = name
                pizza.ingredients = ingredients
                db.session.commit()

                response = make_response(jsonify({'message': 'Pizza updated successfully'}), 200)
            else:
                response = make_response(jsonify({'error': 'Missing required fields'}), 400)
        else:
            response = make_response(jsonify({'error': 'Pizza not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def delete(self, id):
        pizza = db.session.query(Pizza).filter_by(id=id).first()

        if pizza:
            db.session.delete(pizza)
            db.session.commit()

            response = make_response(jsonify({'message': 'Pizza deleted successfully'}), 200)
        else:
            response = make_response(jsonify({'error': 'Pizza not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response


class RestaurantPizzaResource(Resource):
    def get(self, id=None):
        if id is None:
            return self.get_all()
        else:
            return self.get_by_id(id)

    def get_by_id(self, id):
        restaurant_pizza = db.session.query(RestaurantPizza).filter_by(id=id).first()

        if restaurant_pizza:
            restaurant_pizza_obj = {
                'price': restaurant_pizza.price
            }
            response = make_response(jsonify(restaurant_pizza_obj), 200)
        else:
            response = make_response(jsonify({'error': 'RestaurantPizza not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def get_all(self):
        restaurant_pizzas = db.session.query(RestaurantPizza).all()
        restaurant_pizza_list = [{'id': pizza.id, 'price': pizza.price} for pizza in restaurant_pizzas]
        response = make_response(jsonify(restaurant_pizza_list), 200)
        response.headers.set('Content-Type', 'application/json')
        return response

    def post(self):
        data = request.get_json()
        restaurant_id = data.get('restaurant_id')
        pizza_id = data.get('pizza_id')
        price = data.get('price')

        if not (restaurant_id and pizza_id and price):
            response = make_response(jsonify({'error': 'Missing required fields'}), 400)
        else:
            restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
            pizza = db.session.query(Pizza).filter_by(id=pizza_id).first()

            if restaurant and pizza:
                restaurant_pizza = RestaurantPizza(restaurant_id=restaurant_id, pizza_id=pizza_id, price=price)
                db.session.add(restaurant_pizza)
                db.session.commit()
                response = make_response(jsonify({'message': 'RestaurantPizza created successfully'}), 201)
            else:
                response = make_response(jsonify({'error': 'Restaurant or Pizza not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def put(self, id):
        restaurant_pizza = db.session.query(RestaurantPizza).filter_by(id=id).first()

        if restaurant_pizza:
            data = request.get_json()
            price = data.get('price')

            if price:
                restaurant_pizza.price = price
                db.session.commit()

                response = make_response(jsonify({'message': 'RestaurantPizza updated'}), 200)
            else:
                response = make_response(jsonify({'error': 'Missing fields'}), 400)
        else:
            response = make_response(jsonify({'error': 'Not found'}), 404)

        response.headers['Content-Type'] = 'application/json'
        return response

    def delete(self, id):
        restaurant_pizza = db.session.query(RestaurantPizza).filter_by(id=id).first()

        if restaurant_pizza:
            db.session.delete(restaurant_pizza)
            db.session.commit()
            message = 'RestaurantPizza deleted successfully'
            status_code = 200
        else:
            message = 'RestaurantPizza not found'
            status_code = 404

        response = make_response(jsonify({'message': message}), status_code)
        response.headers['Content-Type'] = 'application/json'
        return response



api.add_resource(Home, '/')
api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:id>')
api.add_resource(PizzaResource, '/pizzas', '/pizzas/<int:id>')
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas', '/restaurant_pizzas/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)