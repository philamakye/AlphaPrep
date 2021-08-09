from flask import Flask
from datetime import timedelta

#set up routes import
from .main.routes import main
from .users.routes import users
from .tests.routes import tests
from .tutorials.routes import tutorials

#importing extensions
from .extensions import *

from .util.filters import filter_shuffle


def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config.DevelopmentConfig')
    
    #initialzing extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    mysql.init_app(app)
    
    login_manager.login_view = 'main.login'
    
    
    with app.app_context():
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(tests)
        app.register_blueprint(tutorials)
        
        #registering filters
        app.jinja_env.filters['filter_shuffle'] = filter_shuffle
        
        
        app.permanent_session_lifetime = timedelta(minutes=300)	
    
    return app