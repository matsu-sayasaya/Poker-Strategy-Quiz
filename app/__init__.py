from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder='static',
                template_folder=os.path.abspath('templates'))
    app.config.from_object(config_class)

    from app import routes
    app.register_blueprint(routes.bp)

    return app

