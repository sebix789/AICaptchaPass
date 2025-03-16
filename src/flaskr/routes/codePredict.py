from flask import jsonify, Blueprint, request
from paddleocr import PaddleOCR
import base64
from io import BytesIO
from PIL import Image
import os
import shutil

codePredict = Blueprint('codePredict', __name__)
ocr = PaddleOCR(lang="en")

@codePredict.route('/codePredict', methods=['POST'])
def code_predict():
    try:
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400
        
        if image_data.startswith('data:image/png;base64,'):
            image_data = image_data.replace('data:image/png;base64,', '')
            
        image_data = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_data))

        temp_folder = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_folder, exist_ok=True)
        temp_image_path = os.path.join(temp_folder, 'temp_image.png')
        image.save(temp_image_path)

        results = ocr.ocr(temp_image_path)

        modelPrediction = []
        if results:
            for line in results:
                if line:
                    for word_info in line:
                        if len(word_info) >= 2 and isinstance(word_info[1], tuple):
                            text, confidence = word_info[1]
                            modelPrediction.append(text)

        shutil.rmtree(temp_folder)
        modelPredictionString = " ".join(modelPrediction)
        
        return jsonify({"modelPrediction": modelPredictionString})

    except Exception as e:
        return jsonify({"error": str(e)}), 500