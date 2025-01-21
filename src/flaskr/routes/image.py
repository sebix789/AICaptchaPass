from flask import Blueprint, send_file
from src.flaskr.db import get_db
from bson.objectid import ObjectId
from gridfs import GridFS

image = Blueprint('image', __name__)

database = get_db()


@image.route('/image/<string:collection_name>/<string:file_id>')
def get_image(collection_name, file_id):
    fs = GridFS(database, collection=collection_name)
    try:
        file = fs.get(ObjectId(file_id))
        return send_file(file, download_name=file.filename)
    except Exception as e:
        return f"Error during image download: {e}", 404
