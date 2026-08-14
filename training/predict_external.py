from pathlib import Path
import csv

import numpy as np
import tensorflow as tf
from PIL import Image

from dataset_config import (
    RAW_TEST_DIR,
    CLASS_NAMES,
    IMAGE_SIZE,
)


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "signavision_cnn_best.keras"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "external_test"
)

RESULTS_FILE = (
    OUTPUT_DIR
    / "external_predictions.csv"
)


# ============================================================
# Configuration
# ============================================================

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def get_expected_label(filename):
    """
    Convert:

        A_test.jpg
        B_test.jpg
        nothing_test.jpg
        space_test.jpg

    into:

        A
        B
        nothing
        space
    """

    stem = Path(filename).stem

    if stem.endswith("_test"):
        return stem[:-5]

    return stem


def load_image(image_path):
    """
    Load and preprocess one image.

    The model itself performs pixel normalization,
    so here we only resize and convert to RGB.
    """

    image = Image.open(
        image_path
    ).convert("RGB")

    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.array(
        image,
        dtype=np.float32,
    )

    image_array = np.expand_dims(
        image_array,
        axis=0,
    )

    return image_array


def predict_image(
    model,
    image_path,
):
    """
    Run one image through the CNN.
    """

    image = load_image(
        image_path
    )

    probabilities = model.predict(
        image,
        verbose=0,
    )[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    predicted_class = (
        CLASS_NAMES[predicted_index]
    )

    confidence = float(
        probabilities[predicted_index]
    )

    # Top 3 predictions
    top_indices = np.argsort(
        probabilities
    )[-3:][::-1]

    top_predictions = []

    for index in top_indices:

        top_predictions.append(
            {
                "class": CLASS_NAMES[index],
                "confidence": float(
                    probabilities[index]
                ),
            }
        )

    return (
        predicted_class,
        confidence,
        top_predictions,
    )


def main():

    print("=" * 80)
    print(
        "SignaVision - External Image Inference"
    )
    print("=" * 80)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    print(
        "\nLoading trained CNN..."
    )

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model not found:\n{MODEL_PATH}"
        )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Model loaded successfully."
    )

    # --------------------------------------------------------
    # Find images
    # --------------------------------------------------------

    image_files = sorted(
        [
            file
            for file in RAW_TEST_DIR.iterdir()
            if (
                file.is_file()
                and file.suffix.lower()
                in VALID_EXTENSIONS
            )
        ]
    )

    if not image_files:

        raise FileNotFoundError(
            f"No images found in:\n"
            f"{RAW_TEST_DIR}"
        )

    print(
        f"\nFound {len(image_files)} "
        "external images."
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    results = []

    correct_predictions = 0

    print(
        "\n" + "-" * 80
    )

    print(
        f"{'IMAGE':<25}"
        f"{'EXPECTED':<15}"
        f"{'PREDICTED':<15}"
        f"{'CONFIDENCE':<15}"
        f"{'RESULT'}"
    )

    print(
        "-" * 80
    )

    for image_path in image_files:

        expected_class = (
            get_expected_label(
                image_path.name
            )
        )

        (
            predicted_class,
            confidence,
            top_predictions,
        ) = predict_image(
            model,
            image_path,
        )

        is_correct = (
            predicted_class
            == expected_class
        )

        if is_correct:
            correct_predictions += 1

        result = (
            "✓ CORRECT"
            if is_correct
            else "✗ WRONG"
        )

        print(
            f"{image_path.name:<25}"
            f"{expected_class:<15}"
            f"{predicted_class:<15}"
            f"{confidence:>10.2%}     "
            f"{result}"
        )

        results.append(
            {
                "image": image_path.name,
                "expected": expected_class,
                "predicted": predicted_class,
                "confidence": confidence,
                "correct": is_correct,
                "top_1": top_predictions[0]["class"],
                "top_1_confidence":
                    top_predictions[0][
                        "confidence"
                    ],
                "top_2": top_predictions[1]["class"],
                "top_2_confidence":
                    top_predictions[1][
                        "confidence"
                    ],
                "top_3": top_predictions[2]["class"],
                "top_3_confidence":
                    top_predictions[2][
                        "confidence"
                    ],
            }
        )

    # --------------------------------------------------------
    # External accuracy
    # --------------------------------------------------------

    external_accuracy = (
        correct_predictions
        / len(image_files)
    )

    # --------------------------------------------------------
    # Save CSV
    # --------------------------------------------------------

    fieldnames = [
        "image",
        "expected",
        "predicted",
        "confidence",
        "correct",
        "top_1",
        "top_1_confidence",
        "top_2",
        "top_2_confidence",
        "top_3",
        "top_3_confidence",
    ]

    with open(
        RESULTS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        "\n" + "=" * 80
    )

    print(
        "EXTERNAL TEST COMPLETE"
    )

    print(
        "=" * 80
    )

    print(
        f"\nCorrect predictions: "
        f"{correct_predictions}/"
        f"{len(image_files)}"
    )

    print(
        f"External accuracy: "
        f"{external_accuracy:.2%}"
    )

    print(
        f"\nResults saved to:\n"
        f"{RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()