import os
from flask import Flask

from src.flaskr.routes.main import main

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        env = os.environ.get('FLASK_ENV', 'development')
        if env == 'production':
            app.config.from_pyfile('config_prod.py', silent=True)
        elif env == 'testing':
            app.config.from_pyfile('config_test.py', silent=True)
        else:
            app.config.from_pyfile('config_dev.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # REGISTER ROUTES
    app.register_blueprint(main)

    return app
