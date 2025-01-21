from flask import Blueprint, jsonify
from src.flaskr.services.generateImageCaptcha import generateCaptcha

imageCaptcha = Blueprint('imageCaptcha', __name__)


@imageCaptcha.route('/image-captcha/<string:category_id>')
def get_categories(category_id):
    try:
        generatedCaptcha = generateCaptcha(category_id)

        return jsonify(generatedCaptcha)
    except Exception as e:
        return jsonify({"error": f"Unable to fetch data: {e}"}), 500
