from flask import Flask
from flask_pymongo import PyMongo

# Load environment variables from .env file
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    mongo.init_app(app)

    # Set up config, register blueprints, initialize db etc.
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.risk import bp as risk_bp
    app.register_blueprint(risk_bp, url_prefix='/risk')

    from app.routes.news import bp as news_bp
    app.register_blueprint(news_bp, url_prefix='/news')
    
    return app
