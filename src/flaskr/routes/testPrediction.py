from flask import Blueprint, jsonify
import tensorflow as tf
import json
import os
from datetime import datetime
from gridfs import GridFS
import random
from src.flaskr.db import get_db
# from src.models.model import load_model
from src.utils.functions.labelMap import format_prediction

testPrediction = Blueprint('testPrediction', __name__)

def get_random_image():
    db = get_db()

    # Get a random category
    categories = list(db.categories.find())
    if not categories:
        raise ValueError("No categories found in the database.")

    random_category = random.choice(categories)
    category_id = random_category['_id']

    # Get an image from the corresponding GridFS collection
    fs = GridFS(db, collection=f"category_{category_id}")
    image_file = fs.find_one()
    if image_file is None:
        raise ValueError(f"No images found in the category: {category_id}.")

    return {
        'id': str(image_file._id),
        'data': image_file.read(),
        'label': category_id  # Assuming label is the category ID
    }

def save_to_json(image_data, prediction):
    result = {
        'timestamp': datetime.now().isoformat(),
        'image_id': image_data['id'],
        'true_label': image_data['label'],
        'predicted_label': prediction,
    }

    filename = 'test_results.json'
    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)

    return result

@testPrediction.route('/test-prediction')
def test_prediction():
    try:
        # Get random image
#         image_data = get_random_image()
#
#         # Load and preprocess image
#         image = tf.image.decode_jpeg(image_data['data'], channels=3)
#         image = tf.image.resize(image, [299, 299])
#         image = image / 255.0
#         image = tf.expand_dims(image, 0)  # Add batch dimension
#
#         # Load model and make prediction
#         model = load_model()
#         prediction = model.predict(image)
#
#         pred_class = str(prediction.argmax())
#         formatted_prediction = format_prediction(pred_class)
#
#         # Save results
#         result = save_to_json(image_data, formatted_prediction)
#
#         return jsonify(result)
          return jsonify('{}')

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
