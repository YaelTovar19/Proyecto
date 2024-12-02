from app import app
from api.extensions import db

with app.app_context():
    db.create_all()
    print("Base de datos actualizada con éxito.")
