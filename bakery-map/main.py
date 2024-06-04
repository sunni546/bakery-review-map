from flask import Flask
from flask_cors import CORS
from flask_restx import Api

app = Flask(__name__)
CORS(app)

api = Api(
    app,
    version='0.1',
    title="Bakery-Map",
    description="Bakery Map Project.",
    terms_url="/"
)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
