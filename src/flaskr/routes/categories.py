from flask import Blueprint, jsonify
from src.flaskr.db import get_db

categories = Blueprint('categories', __name__)


@categories.route('/categories')
def get_categories():
    try:
        database = get_db()
        data = list(database.categories.find())

        for item in data:
            item['_id'] = str(item['_id'])

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Unable to fetch data: {e}"}), 500
