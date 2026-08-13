import tensorflow as tf

from dataset_config import (
    TRAIN_DIR,
    VALIDATION_DIR,
    TEST_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    CLASS_NAMES,
    RANDOM_SEED,
)


def load_dataset(
    directory,
    shuffle=True,
):
    """
    Load images from a directory structure such as:

    directory/
        A/
        B/
        C/
        ...
        Z/
        del/
        nothing/
        space/

    Returns a TensorFlow Dataset.
    """

    dataset = tf.keras.utils.image_dataset_from_directory(
        directory=str(directory),
        labels="inferred",
        label_mode="categorical",
        class_names=CLASS_NAMES,
        color_mode="rgb",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        seed=RANDOM_SEED,
    )

    return dataset


def prepare_dataset(dataset):
    """
    Optimize the TensorFlow input pipeline.
    """

    dataset = dataset.cache()

    dataset = dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    return dataset


def load_train_dataset():
    dataset = load_dataset(
        TRAIN_DIR,
        shuffle=True,
    )

    return prepare_dataset(dataset)


def load_validation_dataset():
    dataset = load_dataset(
        VALIDATION_DIR,
        shuffle=False,
    )

    return prepare_dataset(dataset)


def load_test_dataset():
    dataset = load_dataset(
        TEST_DIR,
        shuffle=False,
    )

    return prepare_dataset(dataset)