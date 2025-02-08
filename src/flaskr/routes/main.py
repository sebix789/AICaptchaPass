from flask import Blueprint
from src.flaskr import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    database = db.get_db()
    try:
        database.command('ping')
        return "Hello on main route, connected to database SUCCESSFUL!"
    except Exception as e:
        return f"Hello on main route, ERROR connecting to database: {e}"
