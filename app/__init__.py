from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder=os.path.abspath('templates'),
                static_folder=os.path.abspath('static'))
    app.config.from_object(config_class)

    from app import routes
    app.register_blueprint(routes.bp)

    return app

