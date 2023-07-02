from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import app
# Pass the required route to the decorator.
@app.route("/")
@app.route("/home")
def home():
    return {'message': " Karibu tuone api"
        }





    

if __name__ == '_main_':
    app.run(debug=True, port = 5555)