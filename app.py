import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_jwt_extended import JWTManager
from application.api.auth import auth
from application.api.customer import order
from application.api.admin import admin
from application.logger import logger

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV','development') == 'production':
        raise Exception('Currently no production config is setup.')
    else:
        logger.debug('Starting Local Development')
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(order)
    app.register_blueprint(admin)
    app.app_context().push()
    return app

app = create_app()





if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000')