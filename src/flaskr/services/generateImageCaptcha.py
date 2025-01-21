from gridfs import GridFS
from src.flaskr import get_db
import random
import os

db = get_db()


def read_images(main_category_id="n01443537", num_from_main=2, total_images=9):
    """
    Reads a specified number of images from MongoDB GridFS, with a minimum number
    from a main category and the rest randomly selected from other categories.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              'category': The category ID of the image.
              'filename': The filename of the image.
              'data': The image data (file content) as bytes.
    """
    if num_from_main < 2:
        raise ValueError("num_from_main must be at least 2.")
    if total_images < num_from_main:
        raise ValueError("total_images cannot be less than num_from_main.")

    read_images_data = []

    # 1. Read images from the main category
    main_fs_collection_name = f"category_{main_category_id}"
    main_fs = GridFS(db, collection=main_fs_collection_name)
    main_category_files = list(main_fs.find())
    if not main_category_files:
        print(f"Warning: No images found in the main category: {main_category_id}")
    else:
        num_to_read_main = min(num_from_main, len(main_category_files))
        random_main_images = random.sample(main_category_files, num_to_read_main)
        for file in random_main_images:
            read_images_data.append({
                'category': main_category_id,
                'filename': file.filename,
                'data': file.read(),
                'gridfs_id': str(file._id)
            })

    # 2. Read images from other categories
    remaining_images_needed = total_images - len(read_images_data)
    if remaining_images_needed > 0:
        all_category_ids = [col.split('_')[1] for col in db.list_collection_names() if
                            col.startswith("category_") and len(col.split('_')) > 1]
        unique_numbers = set()
        for item in all_category_ids:
            number = item.replace(".files", "").replace(".chunks", "")
            unique_numbers.add(number)
        all_category_ids_formatted = list(unique_numbers)
        other_category_ids = [cat_id for cat_id in all_category_ids_formatted if cat_id != main_category_id]

        if not other_category_ids:
            print("Warning: No other categories found to fetch remaining images from.")
        else:
            num_other_categories_to_use = min(random.randint(2, 4), len(other_category_ids))
            selected_other_category_ids = random.sample(other_category_ids, num_other_categories_to_use)

            while remaining_images_needed > 0 and selected_other_category_ids:
                other_category_id = random.choice(selected_other_category_ids)  # Wybierz losową kategorię z wybranych
                other_fs_collection_name = f"category_{other_category_id}"
                other_fs = GridFS(db, collection=other_fs_collection_name)
                other_category_files = list(other_fs.find())

                if other_category_files:
                    num_to_read_from_current_other = min(random.randint(1, 3), remaining_images_needed,
                                                         len(other_category_files))
                    random_other_images = random.sample(other_category_files, num_to_read_from_current_other)
                    for file in random_other_images:
                        read_images_data.append({
                            'category': other_category_id,
                            'filename': file.filename,
                            'data': file.read(),
                            'gridfs_id': str(file._id)
                        })
                        remaining_images_needed -= 1
                else:
                    print(f"Warning: No images found in category: {other_category_id}")
                    selected_other_category_ids.remove(other_category_id)  # Usuń kategorię, jeśli jest pusta

                if not selected_other_category_ids:
                    print("Warning: No more other categories with images available.")
                    break

    random.shuffle(read_images_data)

    return read_images_data


def generateCaptcha(category: str):
    images_with_info = read_images(main_category_id=category, num_from_main=2, total_images=9)

    images_result = []

    BACKEND_HOST = os.environ.get('BACKEND_HOST', 'localhost:5000')

    if images_with_info:
        for image_info in images_with_info:
            images_result.append({
                '_id': image_info['filename'].replace('.JPEG', ""),
                'category': image_info['category'],
                'imageUrl': f'{BACKEND_HOST}/image/category_{image_info["category"]}/{image_info["gridfs_id"]}',
                # TODO: HERE WILL BE REAL MODEL PREDICTION IN FEATURE
                "modelPrediction": image_info['category']
            })

    return images_result
