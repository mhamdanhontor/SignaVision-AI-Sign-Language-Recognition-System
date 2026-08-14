from pathlib import Path
import json

import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)

from dataset_config import (
    CLASS_NAMES,
    NUM_CLASSES,
)

from data_loader import (
    load_test_dataset,
)


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "signavision_baseline_cnn.keras"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "model_comparison"
)

METRICS_PATH = (
    OUTPUT_DIR
    / "baseline_metrics.json"
)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 70)
    print("SignaVision - Baseline CNN Evaluation")
    print("=" * 70)

    print("\nLoading baseline model...")

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded.")

    print("\nLoading test dataset...")

    test_dataset = load_test_dataset()

    # --------------------------------------------------------
    # Keras evaluation
    # --------------------------------------------------------

    results = model.evaluate(
        test_dataset,
        verbose=1,
        return_dict=True,
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    true_labels = []
    predicted_labels = []

    for images, labels in test_dataset:

        predictions = model.predict(
            images,
            verbose=0,
        )

        predicted = np.argmax(
            predictions,
            axis=1,
        )

        actual = np.argmax(
            labels.numpy(),
            axis=1,
        )

        predicted_labels.extend(
            predicted
        )

        true_labels.extend(
            actual
        )

    true_labels = np.array(
        true_labels
    )

    predicted_labels = np.array(
        predicted_labels
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = np.mean(
        true_labels
        == predicted_labels
    )

    precision = precision_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0,
    )

    metrics = {
        "test_accuracy": float(
            accuracy
        ),

        "weighted_precision": float(
            precision
        ),

        "weighted_recall": float(
            recall
        ),

        "weighted_f1_score": float(
            f1
        ),

        "test_samples": int(
            len(true_labels)
        ),

        "number_of_classes": (
            NUM_CLASSES
        ),

        "loss": float(
            results["loss"]
        ),

        "keras_accuracy": float(
            results["accuracy"]
        ),

        "top_3_accuracy": float(
            results["top_3_accuracy"]
        ),

        "parameter_count": int(
            model.count_params()
        ),
    }

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
        )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("BASELINE EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"\nTest Accuracy: "
        f"{accuracy:.4%}"
    )

    print(
        f"Precision: "
        f"{precision:.4%}"
    )

    print(
        f"Recall: "
        f"{recall:.4%}"
    )

    print(
        f"F1 Score: "
        f"{f1:.4%}"
    )

    print(
        f"Top-3 Accuracy: "
        f"{results['top_3_accuracy']:.4%}"
    )

    print(
        f"Parameters: "
        f"{model.count_params():,}"
    )

    print(
        f"\nSaved:\n"
        f"{METRICS_PATH}"
    )


if __name__ == "__main__":
    main()