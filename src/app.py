from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.controllers import Users, Restaurants, Reservations, Menus
from flask_restful import Api
from api.models import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api.add_resource(Users, "/api/users", "/api/users/<int:user_id>")
api.add_resource(Restaurants, "/api/restaurants", "/api/restaurants/<int:restaurant_id>")
api.add_resource(Reservations, "/api/reservations", "/api/reservations/<int:reservation_id>")
api.add_resource(Menus, "/api/menus", "/api/menus/<int:menu_id>")

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)
