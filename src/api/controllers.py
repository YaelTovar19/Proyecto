from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask import request
from .models import UserModel, RestaurantModel, ReservationModel, MenuModel, db
from datetime import datetime

# Parsers para Usuarios
user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True, help="Nombre de usuario es obligatorio.")
user_args.add_argument("email", type=str, required=True, help="El correo electrónico es obligatorio.")
user_args.add_argument("password", type=str, required=True, help="Contraseña obligatoria.")

# Parsers para Restaurantes
restaurant_args = reqparse.RequestParser()
restaurant_args.add_argument("name", type=str, required=True)
restaurant_args.add_argument("location", type=str, required=True)
restaurant_args.add_argument("max_capacity", type=int, required=True)

# Parsers para Reservaciones
reservation_args = reqparse.RequestParser()
reservation_args.add_argument("user_id", type=int, required=True)
reservation_args.add_argument("restaurant_id", type=int, required=True)
reservation_args.add_argument("reservation_date", type=str, required=True)
reservation_args.add_argument("guests", type=int, required=True)

# Parsers para Menús
menu_args = reqparse.RequestParser()
menu_args.add_argument("restaurant_id", type=int, required=True, help="ID del restaurante es obligatorio.")
menu_args.add_argument("name", type=str, required=True, help="El nombre del menú es obligatorio.")
menu_args.add_argument("description", type=str, help="Descripción opcional del menú.")
menu_args.add_argument("price", type=float, required=True, help="El precio es obligatorio.")

# Campos para Usuarios
user_fields = {"id": fields.Integer, "username": fields.String, "email": fields.String, "password": fields.String}

# Campos para Restaurantes
restaurant_fields = {"id": fields.Integer, "name": fields.String, "location": fields.String, "max_capacity": fields.Integer}

# Campos para Reservaciones
reservation_fields = {"id": fields.Integer, "user_id": fields.Integer, "restaurant_id": fields.Integer, "reservation_date": fields.String, "guests": fields.Integer}

# Campos para Menús
menu_fields = {"id": fields.Integer, "restaurant_id": fields.Integer, "name": fields.String, "description": fields.String, "price": fields.Float}

class Users(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.get(user_id)
            if not user:
                abort(404, message="User not found")
            return user
        users = UserModel.query.all()
        return users, 200

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_args.parse_args()
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return user, 200

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

class Restaurants(Resource):
    @marshal_with(restaurant_fields)
    def post(self):
        args = restaurant_args.parse_args()
        restaurant = RestaurantModel(name=args['name'], location=args['location'], max_capacity=args['max_capacity'])
        db.session.add(restaurant)
        db.session.commit()
        return restaurant, 201

    @marshal_with(restaurant_fields)
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = RestaurantModel.query.get(restaurant_id)
            if not restaurant:
                abort(404, message="Restaurant not found")
            return restaurant
        restaurants = RestaurantModel.query.all()
        return restaurants, 200

    @marshal_with(restaurant_fields)
    def put(self, restaurant_id):
        args = restaurant_args.parse_args()
        restaurant = RestaurantModel.query.get(restaurant_id)
        if not restaurant:
            abort(404, message="Restaurant not found")
        restaurant.name = args['name']
        restaurant.location = args['location']
        restaurant.max_capacity = args['max_capacity']
        db.session.commit()
        return restaurant, 200

    def delete(self, restaurant_id):
        restaurant = RestaurantModel.query.get(restaurant_id)
        if not restaurant:
            abort(404, message="Restaurant not found")
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

class Reservations(Resource):
    @marshal_with(reservation_fields)
    def post(self):
        args = reservation_args.parse_args()
        reservation_date = datetime.strptime(args['reservation_date'], "%Y-%m-%dT%H:%M:%S")
        reservation = ReservationModel(
            user_id=args['user_id'], restaurant_id=args['restaurant_id'], reservation_date=reservation_date, guests=args['guests']
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation, 201

    @marshal_with(reservation_fields)
    def get(self, reservation_id=None):
        if reservation_id:
            reservation = ReservationModel.query.get(reservation_id)
            if not reservation:
                abort(404, message="Reservation not found")
            return reservation
        reservations = ReservationModel.query.all()
        return reservations, 200

    def delete(self, reservation_id):
        reservation = ReservationModel.query.get(reservation_id)
        if not reservation:
            abort(404, message="Reservation not found")
        db.session.delete(reservation)
        db.session.commit()
        return '', 204

class Menus(Resource):
    @marshal_with(menu_fields)
    def post(self):
        args = menu_args.parse_args()
        menu = MenuModel(
            restaurant_id=args['restaurant_id'],
            name=args['name'],
            description=args['description'],
            price=args['price']
        )
        db.session.add(menu)
        db.session.commit()
        return menu, 201

    @marshal_with(menu_fields)
    def get(self, menu_id=None):
        if menu_id:
            menu = MenuModel.query.get(menu_id)
            if not menu:
                abort(404, message="Menu not found")
            return menu
        menus = MenuModel.query.all()
        return menus, 200
