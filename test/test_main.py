from datetime import datetime
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from src.api.models import db
from src.api.controllers import Users, Restaurants, Reservations, Menus

class TestRestaurantReservationSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the Flask application
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(cls.app)
        api = Api(cls.app)
        
        # Register the routes
        api.add_resource(Users, '/api/users', '/api/users/<int:user_id>')
        api.add_resource(Restaurants, '/api/restaurants', '/api/restaurants/<int:restaurant_id>')
        api.add_resource(Reservations, '/api/reservations', '/api/reservations/<int:reservation_id>')
        api.add_resource(Menus, '/api/menus', '/api/menus/<int:menu_id>')

        cls.client = cls.app.test_client()
        
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.client.post('/api/users', json={
            'username': 'User',
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_user_not_found(self):
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)

    def test_get_users(self):
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_user(self):
        self.client.post('/api/users', json={
            'username': 'Old Name',
            'email': 'oldemail@example.com',
            'password': 'oldpassword'
        })
        response = self.client.put('/api/users/1', json={
            'username': 'Updated Name',
            'email': 'updatedemail@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'Updated Name')

    def test_delete_user(self):
        self.client.post('/api/users', json={
            'username': 'User',
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        response = self.client.delete('/api/users/1')
        self.assertIn(response.status_code, [204, 404])

    def test_create_restaurant(self):
        response = self.client.post('/api/restaurants', json={
            'name': 'Test Restaurant',
            'location': '123 Test St',
            'max_capacity': 50
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_restaurants(self):
        response = self.client.get('/api/restaurants')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_reservation(self):
        self.client.post('/api/users', json={
            'username': 'Test User',
            'email': 'testuser2@example.com',
            'password': 'password2'
        })
        self.client.post('/api/restaurants', json={
            'name': 'Another Restaurant',
            'location': '456 Another St',
            'max_capacity': 100
        })
        response = self.client.post('/api/reservations', json={
            'user_id': 1,
            'restaurant_id': 1,
            'reservation_date': '2024-12-31T20:00:00',
            'guests': 4
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_reservations(self):
        response = self.client.get('/api/reservations')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_delete_reservation(self):
        self.client.post('/api/reservations', json={
            'user_id': 1,
            'restaurant_id': 1,
            'reservation_date': '2024-12-31T20:00:00',
            'guests': 4
        })
        response = self.client.delete('/api/reservations/1')
        self.assertIn(response.status_code, [204, 404])

if __name__ == '__main__':
    unittest.main()
