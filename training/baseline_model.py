import tensorflow as tf

from dataset_config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    IMAGE_CHANNELS,
    NUM_CLASSES,
)


def build_baseline_cnn():
    """
    Lightweight baseline CNN used for comparison
    against the SignaVision Custom CNN.

    The architecture is intentionally smaller.
    """

    inputs = tf.keras.Input(
        shape=(
            IMAGE_HEIGHT,
            IMAGE_WIDTH,
            IMAGE_CHANNELS,
        ),
        name="image_input",
    )

    # --------------------------------------------------------
    # Normalization
    # --------------------------------------------------------

    x = tf.keras.layers.Rescaling(
        1.0 / 255.0,
        name="pixel_normalization",
    )(inputs)

    # --------------------------------------------------------
    # Convolution Block 1
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        activation="relu",
        name="conv1",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        (2, 2),
        name="pool1",
    )(x)

    # --------------------------------------------------------
    # Convolution Block 2
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        activation="relu",
        name="conv2",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        (2, 2),
        name="pool2",
    )(x)

    # --------------------------------------------------------
    # Feature Aggregation
    # --------------------------------------------------------

    x = tf.keras.layers.GlobalAveragePooling2D(
        name="global_average_pooling",
    )(x)

    # --------------------------------------------------------
    # Dense Layer
    # --------------------------------------------------------

    x = tf.keras.layers.Dense(
        128,
        activation="relu",
        name="dense_features",
    )(x)

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="classification",
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="SignaVision_Baseline_CNN",
    )

    return model


def compile_baseline_model(model):

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001,
        ),
        loss="categorical_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.TopKCategoricalAccuracy(
                k=3,
                name="top_3_accuracy",
            ),
        ],
    )

    return model


if __name__ == "__main__":

    model = build_baseline_cnn()

    model = compile_baseline_model(
        model
    )

    model.summary()