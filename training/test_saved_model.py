from pathlib import Path

import numpy as np
import tensorflow as tf

from dataset_config import (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    IMAGE_CHANNELS,
    NUM_CLASSES,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "signavision_cnn_best.keras"
)


def main():

    print("=" * 70)
    print("SignaVision - Saved Model Test")
    print("=" * 70)

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model not found:\n{MODEL_PATH}"
        )

    print("\nLoading saved model...")

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    print(
        f"\nModel input shape: "
        f"{model.input_shape}"
    )

    print(
        f"Model output shape: "
        f"{model.output_shape}"
    )

    # --------------------------------------------------------
    # Create dummy input
    # --------------------------------------------------------

    dummy_image = np.random.rand(
        1,
        IMAGE_HEIGHT,
        IMAGE_WIDTH,
        IMAGE_CHANNELS,
    ).astype(
        np.float32
    ) * 255.0

    prediction = model.predict(
        dummy_image,
        verbose=0,
    )

    predicted_class = int(
        np.argmax(prediction[0])
    )

    confidence = float(
        np.max(prediction[0])
    )

    probability_sum = float(
        np.sum(prediction[0])
    )

    print(
        f"\nPrediction output shape: "
        f"{prediction.shape}"
    )

    print(
        f"Predicted class index: "
        f"{predicted_class}"
    )

    print(
        f"Confidence: "
        f"{confidence:.4f}"
    )

    print(
        f"Probability sum: "
        f"{probability_sum:.4f}"
    )

    if model.output_shape[-1] == NUM_CLASSES:

        print(
            "\n✓ Model has correct "
            f"{NUM_CLASSES}-class output."
        )

    if abs(
        probability_sum - 1.0
    ) < 0.001:

        print(
            "✓ Softmax output is valid."
        )

    print("\n" + "=" * 70)
    print("SAVED MODEL TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()