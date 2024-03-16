import jdk
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/final'

    mongo.init_app(app)

    jdk.install('8', jre=True)

    # Set up config, register blueprints, initialize db etc.
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.risk import bp as risk_bp
    app.register_blueprint(risk_bp, url_prefix='/risk')

    return app
