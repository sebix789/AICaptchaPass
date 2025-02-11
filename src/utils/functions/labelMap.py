import json
import os

def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


def create_classes():
    wnids_file_path = get_absolute_path('../../data/tiny-imagenet-200/wnids.txt')
    words_file_path = get_absolute_path('../../data/tiny-imagenet-200/words.txt')
    classes_path = get_absolute_path('classes.json')

    with open(wnids_file_path, 'r') as f:
        class_ids = [line.strip() for line in f]

    id_to_label = {}
    with open(words_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            class_id = parts[0]
            label = parts[1]
            id_to_label[class_id] = label

    classes = {
        str(index): {"id": class_id, "label": id_to_label.get(class_id, "Unknown class")}
        for index, class_id in enumerate(class_ids)
    }

    with open(classes_path, 'w') as f:
        json.dump(classes, f, indent=4)
        

def load_classes():
    classes_path = get_absolute_path('classes.json')
    if not os.path.exists(classes_path):
        create_classes()
    
    with open(classes_path, 'r') as f:
        classes = json.load(f)
    
    return classes

def format_prediction(pred_class):
    classes = load_classes()
    class_info = classes.get(pred_class, {"id": "Unknown", "label": "Unknown"})
    return f"{class_info['id']} {class_info['label']}"