from flask import Blueprint, jsonify
import os
from paddleocr import PaddleOCR

testOCR = Blueprint('testOCR', __name__)
ocr = PaddleOCR(lang="en")

@testOCR.route('/predict', methods=['GET'])
def test_ocr():
    folder_path = r'C:\Users\Sebastian\Desktop\Moje_pliki\dev\ai\datasets\IIIT5K-Word\combined'
    if not os.path.exists(folder_path):
        return jsonify({"error": f"Folder not found: {folder_path}"}), 404

    total_files = 0
    correct_predictions = 0

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            total_files += 1
            image_path = os.path.join(folder_path, file_name)
            results = ocr.ocr(image_path)

            print(f"OCR Results for {file_name}:", results)

            predictions = []
            if results:
                for line in results:
                    if line:
                        for word_info in line:
                            if len(word_info) >= 2 and isinstance(word_info[1], tuple):
                                text, confidence = word_info[1]
                                predictions.append(text.lower())

            file_name_without_ext = os.path.splitext(file_name)[0].lower()
            if file_name_without_ext in predictions:
                correct_predictions += 1

    if total_files == 0:
        return jsonify({"error": "No valid image files found in the folder"}), 400

    accuracy = correct_predictions / total_files
    print(f"Accuracy: {accuracy * 100:.2f}%")

    return jsonify({"total_files": total_files, "correct_predictions": correct_predictions, "accuracy": accuracy})