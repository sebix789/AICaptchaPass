import tensorflow as tf
import os
import random
import matplotlib.pyplot as plt
import numpy as np
DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Synth90K'))
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")

def preprocess_textimage(image, label, is_Training=True):
    if is_Training:
        image = tf.image.random_brightness(image, max_delta=0.1)
        image = tf.image.random_contrast(image, lower=0.7, upper=1.3)
        image = tf.image.random_crop(image, size=[28, 96, 3])
        noise = tf.random.normal(shape=tf.shape(image), mean=0.0, stddev=0.1)
        image = tf.clip_by_value(image + noise, 0.0, 1.0)
        rotations = random.choice([0, 1, 2, 3])  # Rotate by 0, 90, 180, or 270 degrees
        image = tf.image.rot90(image, k=rotations)

    image = image / 255.0  
    label = tf.strings.unicode_split(label, 'UTF-8')  
    return image, label

def load_labels(labels_file_path):
    image_paths = []
    labels = []
    with open(labels_file_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(" ")
            image_path = os.path.join(DATASET_DIR, parts[0])
            label = " ".join(parts[1:])
            image_paths.append(image_path)
            labels.append(label)
    return image_paths, labels

def get_train_dataset(labels_file, batch_size=32):
    image_paths, labels = load_labels(labels_file)
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    def load_and_preprocess(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        return preprocess_textimage(image, label, is_Training=True)

    dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(buffer_size=1024)
    dataset = dataset.batch(batch_size)
    return dataset

def get_val_dataset(labels_file, batch_size=32):
    image_paths, labels = load_labels(labels_file)
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    def load_and_preprocess(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        return preprocess_textimage(image, label, is_Training=False)

    dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    return dataset

TRAIN_LABELS_FILE = os.path.join(DATASET_DIR, 'train_labels.txt')  
VAL_LABELS_FILE = os.path.join(DATASET_DIR, 'val_labels.txt') 

train_dataset = get_train_dataset(TRAIN_LABELS_FILE, batch_size=32)
val_dataset = get_val_dataset(VAL_LABELS_FILE, batch_size=32)


 ### EXAMPLE SHOW IMAGES ###
#for images, labels in train_dataset.take(1):
 #   plt.figure(figsize=(10, 10))
  #  for i in range(min(images.shape[0], 32)):
   #     plt.subplot(4, 8, i + 1)
    #    plt.imshow(images[i].numpy())
     #   label = ''.join([chr(c) for c in labels[i].numpy()])
      #  plt.title(label)
       # plt.axis("off")
        #plt.show()