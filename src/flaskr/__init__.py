from flask import Flask
from src.flaskr.db import get_db
from src.flaskr.routes.categories import categories
from src.flaskr.routes.main import main
from src.flaskr.routes.imageCaptcha import imageCaptcha
from src.flaskr.routes.image import image
from src.flaskr.routes.testPrediction import testPrediction
import os
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv


load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    try:
        database = get_db()
        database.command('ping')
        print("Connected to database")
    except ConnectionFailure as e:
        print(f"Error during connecting to database: {e}")

    # REGISTER ROUTES
    app.register_blueprint(main)
    app.register_blueprint(categories)
    app.register_blueprint(imageCaptcha)
    app.register_blueprint(image)
    app.register_blueprint(testPrediction, url_prefix='/api')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

    return app

app = create_app()
