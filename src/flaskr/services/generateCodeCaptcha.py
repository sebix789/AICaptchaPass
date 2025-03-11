from flask import Response, send_file
import random
import os
from gridfs import GridFS
from io import BytesIO
from src.flaskr import get_db

db=get_db()



from gridfs import GridFS
import random

def read_codeCaptcha(category=None):
    """Reads a single random image from MongoDB GridFS."""
    fs = GridFS(db,collection='captchas') 

    all_files = list(fs.find()) 
    
    if not all_files:
        raise Exception("No images found in the database")
    

    file = random.choice(all_files)
    

    return {
        'filename': file.filename,
        'data': file.read(), 
        'gridfs_id': str(file._id)  
    }



def generateCodeCaptcha():
    image_info = read_codeCaptcha()
    BACKEND_HOST = os.environ.get('BACKEND_HOST', 'localhost:5000')
    return {
        '_id': image_info['filename'].replace('.JPEG', ""),  
        'imageUrl': f'{BACKEND_HOST}/image/{image_info["gridfs_id"]}', 
        'modelPrediction': image_info['filename'] 
    }
