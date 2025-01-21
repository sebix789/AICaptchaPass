from gridfs import GridFS
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# SETTINGS
CATEGORIES_TO_GET = ["n02231487", "n01443537", 'n01644900', "n02279972", 'n02415577', 'n02481823', 'n02791270']
QUANTITY_OF_ITEM_IN_EACH_CATEGORY_TO_GET = 20

load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', '')

uri = DATABASE_URI
# TODO: tlsAllowInvalidCertificates have to be removed in production code ⬇️
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

db = client[DATABASE_NAME]

train_files_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'tiny-imagenet-200', 'train'))
words_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'tiny-imagenet-200', 'words.txt'))


def upload_data_to_mongodb(categories_data, images_data):
    """
    Uploads image data to MongoDB, creating separate GridFS collections for each category
    and a separate collection for category information, preventing duplicate uploads.

    Args:
        categories_data (dict): A dictionary mapping category IDs to human-readable names.
            Example: {'n01443537': 'goldfish, Carassius auratus', ...}
        images_data (list): A list of dictionaries, where each dictionary contains
            'filename' and 'filepath' of an image.
            Example: [{'filename': '...', 'filepath': '...'}, ...]
        db_name (str): The name of the MongoDB database to use.
    """
    print("Upload images process may take a few seconds...", flush=True)

    # 1. Create or access the 'categories' collection
    categories_collection = db['categories']

    # Insert category information into the 'categories' collection (preventing duplicates)
    for category_id, category_name in categories_data.items():
        if categories_collection.find_one({'_id': category_id}) is None:
            categories_collection.insert_one({'_id': category_id, 'name': category_name})
            print(f"Category '{category_name}' added to the 'categories' collection.")
        else:
            print(f"Category '{category_name}' already exists in the 'categories' collection.")

    # 2. Upload images to separate GridFS collections (preventing duplicates)
    for image_info in images_data:
        filename = image_info['filename']
        filepath = image_info['filepath']

        # Extract the category ID from the filename
        category_id = filename.split('_')[0]

        # Create GridFS object for the specific category collection
        grid_fs_collection_name = f"category_{category_id}"
        fs = GridFS(db, collection=grid_fs_collection_name)

        # Check if the file already exists in the GridFS collection for this category
        if fs.find_one({'filename': filename}) is None:
            try:
                with open(filepath, 'rb') as f:
                    fs.put(f, filename=filename)
                print(f"Uploaded {filename} to GridFS collection: {grid_fs_collection_name}")
            except FileNotFoundError:
                print(f"Error: File not found at {filepath}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")
        else:
            print(f"{filename} already exists in GridFS collection: {grid_fs_collection_name}. Skipping upload.")

    client.close()
    print("Data processing completed.")


def getImages(idsFileArrayToGet, maxImagesPerCategory):
    # Get info
    labels = {}
    try:
        with open(words_path, 'r') as file:
            for line in file:
                key, value = line.strip().split("\t")
                if key in idsFileArrayToGet or len(idsFileArrayToGet) == 0:
                    labels[key] = value
    except FileNotFoundError:
        print(f"Błąd: Plik {words_path} nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    # Get images
    image_files = []

    for folderName, _, _ in os.walk(train_files_path):
        baseNameFolder = os.path.basename(folderName)
        if baseNameFolder != 'images' and (baseNameFolder in idsFileArrayToGet or len(idsFileArrayToGet) == 0):

            for _, _, fileNames in os.walk(os.path.join(folderName, "images")):
                index = 1

                for fileNameEl in fileNames:
                    if index <= maxImagesPerCategory:
                        index += 1
                        image_files.append({
                            'filename': fileNameEl,
                            'filepath': os.path.join(folderName, "images", fileNameEl)
                        })

    return [labels, image_files]


categoryLabels, imageResults = getImages(CATEGORIES_TO_GET, QUANTITY_OF_ITEM_IN_EACH_CATEGORY_TO_GET)

upload_data_to_mongodb(categoryLabels, imageResults)
