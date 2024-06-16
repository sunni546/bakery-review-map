from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from api.bakery import Bakery_api
from api.bread import Bread_api
from api.category import Category_api
from api.interest import Interest_api
from api.level import Level_api
from api.review import Review_api
from api.user import bcrypt, User_api
from config import Config
from models import db

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

bcrypt.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()

authorizations = {'bearer_auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
}}

api = Api(
    app,
    version='0.1',
    title="Bakery-Map",
    description="Bakery Map Project.",
    terms_url="/",
    authorizations=authorizations
)

api.add_namespace(Level_api, '/levels')
api.add_namespace(User_api, '/users')
api.add_namespace(Interest_api, '/interests')
api.add_namespace(Review_api, '/reviews')
api.add_namespace(Bakery_api, '/bakeries')
api.add_namespace(Bread_api, '/breads')
api.add_namespace(Category_api, '/categories')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
