import tensorflow as tf
import os
import random
import numpy as np
import matplotlib.pyplot as plt

DATASET_DIR = os.path.abspath("src/tiny-imagenet-200")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")


def preprocess_image(image, label, is_training=True):
    image = tf.image.resize(image, (224, 224))

    if is_training:
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_brightness(image, max_delta=0.05)
        image = tf.image.random_contrast(image, lower=0.95, upper=1.05)
        image = tf.image.random_saturation(image, lower=0.95, upper=1.05)

        zoom_factor = tf.random.uniform([], minval=0.9, maxval=1.1)
        new_size = tf.cast(tf.shape(image)[0:2], tf.float32) * zoom_factor
        image = tf.image.resize(image, tf.cast(new_size, tf.int32))
        image = tf.image.resize_with_crop_or_pad(image, 224, 224)

        rotations = random.choice([0, 1])
        image = tf.image.rot90(image, k=rotations)

    image = image / 255.0
    label = tf.one_hot(label, 120)
    return image, label


# set labels
wnid_to_label = {}
labelIndex = 0
wnids_path = os.path.join(DATASET_DIR, "wnids.txt")

with open(wnids_path, 'r') as f:
    for line in f:
        wnid = line.strip()
        wnid_to_label[wnid] = labelIndex
        labelIndex += 1


def get_train_dataset(train_dir, batch_size=32):
    image_paths = []
    labels = []
    for wnid, label in wnid_to_label.items():
        images_dir = os.path.join(train_dir, wnid, "images")
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                if filename.endswith(('.JPEG', '.jpg', '.png')):
                    image_paths.append(os.path.join(images_dir, filename))
                    labels.append(label)

    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    def load_and_preprocess(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        return preprocess_image(image, label, is_training=True)

    dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(buffer_size=1024)
    dataset = dataset.batch(batch_size)
    return dataset


def get_val_dataset(val_dir, batch_size=32):
    val_annotations_path = os.path.join(val_dir, "val_annotations.txt")
    image_paths = []
    labels = []

    with open(val_annotations_path, "r") as f:
        for line in f.readlines():
            parts = line.strip().split("\t")
            image_path = os.path.join(val_dir, "images", parts[0])
            label = wnid_to_label.get(parts[1])
            if label is not None:
                image_paths.append(image_path)
                labels.append(label)

    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

    def load_and_preprocess(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        return preprocess_image(image, label, is_training=False)

    dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    return dataset


train_dataset = get_train_dataset(TRAIN_DIR, batch_size=32)
val_dataset = get_val_dataset(VAL_DIR, batch_size=32)


# EXAMPLE SHOW IMAGES
for images, labels in train_dataset.take(1):
    plt.figure(figsize=(10, 10))
    for i in range(images.shape[0]):
        plt.subplot(4, 8, i + 1)
        plt.imshow(images[i].numpy())
        plt.title(np.argmax(labels[i].numpy()))
        plt.axis("off")
    plt.show()
