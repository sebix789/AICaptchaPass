import os
import pymongo
import gridfs
from dotenv import load_dotenv
from io import BytesIO


load_dotenv()


DATABASE_URI = os.environ.get('DATABASE_URI', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', '')
#TODO Add path
#IMAGE_DIR = 
#LABELS_FILE =

client = pymongo.MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]

fs = gridfs.GridFS(db, collection="captchas")


def read_labels_from_file(labels_file):
    """Reads the labels file and returns a list of (filename, label) tuples."""
    labels = []
    with open(labels_file, "r") as file:
        for line in file:
            filename, label = line.strip().split()
            labels.append((filename, label))
    return labels


def upload_image_to_mongodb(image_filename, label):
    """Uploads image to GridFS and stores the label in a MongoDB collection."""
    image_path = os.path.join(IMAGE_DIR, image_filename)
    
 
    if not os.path.exists(image_path):
        print(f"Warning: {image_filename} not found!")
        return


    with open(image_path, "rb") as img_file:
        img_byte_arr = BytesIO(img_file.read())

  
    image_id = fs.put(img_byte_arr, filename=image_filename)

   
    captchas_collection = db['captchas']
    captcha_entry = {
        'captcha_text': label,
        'image_id': image_id  
    }
    captchas_collection.insert_one(captcha_entry)
    print(f"Uploaded {image_filename} with label '{label}' to the database!")


def upload_captchas(labels_file):
    """Uploads all images and labels to MongoDB."""
    labels = read_labels_from_file(labels_file)

    for filename, label in labels:
        upload_image_to_mongodb(filename, label)


if __name__ == "__main__":
    upload_captchas(LABELS_FILE)
