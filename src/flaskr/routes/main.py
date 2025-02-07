from flask import Blueprint
from src.flaskr import db
from src.flaskr.routes.testPrediction import testPrediction

main = Blueprint('main', __name__)
main.register_blueprint(testPrediction, url_prefix='/api')

@main.route('/')
def index():
    database = db.get_db()
    try:
        database.command('ping')
        return "Hello on main route, connected to database SUCCESSFUL!"
    except Exception as e:
        return f"Hello on main route, ERROR connecting to database: {e}"
