import tensorflow as tf

from dataset_config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    IMAGE_CHANNELS,
    NUM_CLASSES,
)


def build_cnn():
    """
    Build the custom SignaVision CNN.

    Input:
        128 x 128 x 3 RGB image

    Output:
        29-class probability distribution
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
    # Input normalization
    # --------------------------------------------------------

    x = tf.keras.layers.Rescaling(
        1.0 / 255.0,
        name="pixel_normalization",
    )(inputs)

    # --------------------------------------------------------
    # Convolution Block 1
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
        use_bias=False,
        name="conv1",
    )(x)

    x = tf.keras.layers.BatchNormalization(
        name="batch_norm1",
    )(x)

    x = tf.keras.layers.ReLU(
        name="relu1",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        name="pool1",
    )(x)

    # --------------------------------------------------------
    # Convolution Block 2
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding="same",
        use_bias=False,
        name="conv2",
    )(x)

    x = tf.keras.layers.BatchNormalization(
        name="batch_norm2",
    )(x)

    x = tf.keras.layers.ReLU(
        name="relu2",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        name="pool2",
    )(x)

    # --------------------------------------------------------
    # Convolution Block 3
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding="same",
        use_bias=False,
        name="conv3",
    )(x)

    x = tf.keras.layers.BatchNormalization(
        name="batch_norm3",
    )(x)

    x = tf.keras.layers.ReLU(
        name="relu3",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        name="pool3",
    )(x)

    # --------------------------------------------------------
    # Convolution Block 4
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding="same",
        use_bias=False,
        name="conv4",
    )(x)

    x = tf.keras.layers.BatchNormalization(
        name="batch_norm4",
    )(x)

    x = tf.keras.layers.ReLU(
        name="relu4",
    )(x)

    x = tf.keras.layers.MaxPooling2D(
        pool_size=(2, 2),
        name="pool4",
    )(x)

    # --------------------------------------------------------
    # Feature Aggregation
    # --------------------------------------------------------

    x = tf.keras.layers.GlobalAveragePooling2D(
        name="global_average_pooling",
    )(x)

    # --------------------------------------------------------
    # Fully Connected Layer
    # --------------------------------------------------------

    x = tf.keras.layers.Dense(
        256,
        activation="relu",
        name="dense_features",
    )(x)

    x = tf.keras.layers.Dropout(
        0.40,
        name="dropout",
    )(x)

    # --------------------------------------------------------
    # Output Layer
    # --------------------------------------------------------

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="classification",
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="SignaVision_CNN",
    )

    return model


def compile_model(model):
    """
    Compile the CNN for 29-class classification.
    """

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

    model = build_cnn()

    model = compile_model(model)

    model.summary()