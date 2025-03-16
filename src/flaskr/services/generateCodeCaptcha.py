import random
import os
from gridfs import GridFS
from src.flaskr import get_db
from gridfs import GridFS
import random
import base64

db=get_db()

def read_codeCaptcha(category=None):
    """Reads a single random image from MongoDB GridFS."""
    
    captchas_collection = db.captchas
    captcha_entry = captchas_collection.aggregate([{ "$sample": { "size": 1 } }]).next()
    
    if not captcha_entry:
        raise Exception("No captchas found in the database")

    fs = GridFS(db, collection='captchas')
    file = fs.get(captcha_entry["image_id"])

    return {
        'filename': file.filename,
        'data': file.read(),
        'gridfs_id': str(file._id),
        'captcha_text': captcha_entry["captcha_text"]
    }

def generateCodeCaptcha():
    image_info = read_codeCaptcha()
    image_base64 = base64.b64encode(image_info['data']).decode('utf-8')
    return {
        '_id': image_info['filename'].replace('.JPEG', ""),
        'image': f"data:image/png;base64,{image_base64}", 
        'captcha_text': image_info['captcha_text']
    }
