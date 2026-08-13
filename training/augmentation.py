import tensorflow as tf

from dataset_config import (
    ROTATION_FACTOR,
    ZOOM_FACTOR,
    TRANSLATION_FACTOR,
    CONTRAST_FACTOR,
)


def create_augmentation_pipeline():
    """
    Data augmentation used only for training images.

    Augmentation helps the CNN generalize to:
    - different hand positions
    - small rotations
    - different camera framing
    - slight zoom differences
    - lighting/contrast changes
    """

    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomRotation(
                factor=ROTATION_FACTOR
            ),

            tf.keras.layers.RandomZoom(
                height_factor=ZOOM_FACTOR,
                width_factor=ZOOM_FACTOR,
            ),

            tf.keras.layers.RandomTranslation(
                height_factor=TRANSLATION_FACTOR,
                width_factor=TRANSLATION_FACTOR,
            ),

            tf.keras.layers.RandomContrast(
                factor=CONTRAST_FACTOR
            ),
        ],
        name="data_augmentation",
    )

    return augmentation