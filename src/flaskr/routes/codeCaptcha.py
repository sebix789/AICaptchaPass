from flask import jsonify, Blueprint


from src.flaskr.services.generateCodeCaptcha import generateCodeCaptcha


codeCaptcha = Blueprint('codeCaptcha', __name__)
@codeCaptcha.route('/codeCaptcha', methods=['GET'])
def get_code_captcha():
    try:
        captcha=generateCodeCaptcha()
        return jsonify(captcha)
    except Exception as e:
        return jsonify({"error":f"error fetching captcha: {e}"}), 500
