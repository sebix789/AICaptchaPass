import os
import pymongo
import gridfs
from dotenv import load_dotenv
from io import BytesIO


load_dotenv()


DATABASE_URI = "mongodb://localhost:27017"  
DATABASE_NAME = "captchaTest"  
IMAGE_DIR = "src\data\Synth90K\cap" 


client = pymongo.MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]

fs = gridfs.GridFS(db, collection="captchas")

def read_label(filename):
    return os.path.splitext(filename)[0]

    



def upload_image_to_mongodb(image_filename):
    """Uploads image to GridFS and stores the label in a MongoDB collection."""
    image_path = os.path.join(IMAGE_DIR, image_filename)
    
 
    if not os.path.exists(image_path):
        print(f"Warning: {image_filename} not found!")
        return


    with open(image_path, "rb") as img_file:
        img_byte_arr = BytesIO(img_file.read())

  
    image_id = fs.put(img_byte_arr, filename=image_filename)
    label = read_label(image_filename) 
    if not label:
        print(f"Skipping {image_filename}: Could not extract label.")
        return


   
    captchas_collection = db['captchas']
    captcha_entry = {
        'captcha_text': label,
        'image_id': image_id  
    }
    captchas_collection.insert_one(captcha_entry)
    print(f"Uploaded {image_filename} with label '{label}' to the database!")


def upload_captchas():
    """Uploads all images and labels to MongoDB."""
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            upload_image_to_mongodb(filename)


if __name__ == "__main__":
    upload_captchas()
