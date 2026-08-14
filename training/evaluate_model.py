from pathlib import Path
import json

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
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


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "signavision_cnn_best.keras"
)

EVALUATION_DIR = (
    PROJECT_ROOT
    / "docs"
    / "evaluation"
)


# ============================================================
# Configuration
# ============================================================

CONFUSION_MATRIX_FILE = (
    EVALUATION_DIR
    / "confusion_matrix.png"
)

CLASS_REPORT_FILE = (
    EVALUATION_DIR
    / "classification_report.txt"
)

METRICS_FILE = (
    EVALUATION_DIR
    / "metrics.json"
)


def create_directories():
    EVALUATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def load_best_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Best model not found:\n{MODEL_PATH}"
        )

    print("\nLoading best CNN model...")

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    return model


def evaluate_test_dataset(
    model,
    test_dataset,
):

    print("\n" + "=" * 70)
    print("TEST DATASET EVALUATION")
    print("=" * 70)

    results = model.evaluate(
        test_dataset,
        verbose=1,
        return_dict=True,
    )

    print("\nTest Results:")

    for metric_name, value in results.items():

        print(
            f"{metric_name}: "
            f"{value:.6f}"
        )

    return results


def collect_predictions(
    model,
    test_dataset,
):

    print("\nGenerating predictions...")

    all_predictions = []
    all_labels = []

    for images, labels in test_dataset:

        predictions = model.predict(
            images,
            verbose=0,
        )

        predicted_classes = np.argmax(
            predictions,
            axis=1,
        )

        true_classes = np.argmax(
            labels.numpy(),
            axis=1,
        )

        all_predictions.extend(
            predicted_classes
        )

        all_labels.extend(
            true_classes
        )

    return (
        np.array(all_labels),
        np.array(all_predictions),
    )


def calculate_metrics(
    true_labels,
    predicted_labels,
):

    accuracy = (
        np.mean(
            true_labels
            == predicted_labels
        )
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
        "test_accuracy": float(accuracy),
        "weighted_precision": float(precision),
        "weighted_recall": float(recall),
        "weighted_f1_score": float(f1),
        "test_samples": int(
            len(true_labels)
        ),
        "number_of_classes": NUM_CLASSES,
    }

    return metrics


def save_classification_report(
    true_labels,
    predicted_labels,
):

    report = classification_report(
        true_labels,
        predicted_labels,
        labels=list(
            range(NUM_CLASSES)
        ),
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0,
    )

    print("\n" + "=" * 70)
    print("CLASSIFICATION REPORT")
    print("=" * 70)

    print(report)

    with open(
        CLASS_REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "SignaVision CNN "
            "Classification Report\n"
        )

        file.write(
            "=" * 70
            + "\n\n"
        )

        file.write(report)


def create_confusion_matrix(
    true_labels,
    predicted_labels,
):

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=list(
            range(NUM_CLASSES)
        ),
    )

    plt.figure(
        figsize=(16, 14)
    )

    plt.imshow(
        matrix,
        interpolation="nearest",
        aspect="auto",
    )

    plt.title(
        "SignaVision CNN - Confusion Matrix"
    )

    plt.colorbar()

    tick_marks = np.arange(
        NUM_CLASSES
    )

    plt.xticks(
        tick_marks,
        CLASS_NAMES,
        rotation=90,
    )

    plt.yticks(
        tick_marks,
        CLASS_NAMES,
    )

    plt.xlabel(
        "Predicted Label"
    )

    plt.ylabel(
        "True Label"
    )

    plt.tight_layout()

    plt.savefig(
        CONFUSION_MATRIX_FILE,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nConfusion matrix saved to:\n"
        f"{CONFUSION_MATRIX_FILE}"
    )


def save_metrics(metrics):

    with open(
        METRICS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
        )

    print(
        f"Metrics saved to:\n"
        f"{METRICS_FILE}"
    )


def main():

    print("=" * 70)
    print("SignaVision - Model Evaluation")
    print("=" * 70)

    create_directories()

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = load_best_model()

    # --------------------------------------------------------
    # Load test dataset
    # --------------------------------------------------------

    print("\nLoading unseen test dataset...")

    test_dataset = load_test_dataset()

    # --------------------------------------------------------
    # Keras evaluation
    # --------------------------------------------------------

    test_results = evaluate_test_dataset(
        model,
        test_dataset,
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    true_labels, predicted_labels = (
        collect_predictions(
            model,
            test_dataset,
        )
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        true_labels,
        predicted_labels,
    )

    # Add Keras metrics
    metrics.update(
        {
            key: float(value)
            for key, value in test_results.items()
        }
    )

    # --------------------------------------------------------
    # Classification report
    # --------------------------------------------------------

    save_classification_report(
        true_labels,
        predicted_labels,
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    create_confusion_matrix(
        true_labels,
        predicted_labels,
    )

    # --------------------------------------------------------
    # Save metrics
    # --------------------------------------------------------

    save_metrics(
        metrics
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"\nTest Accuracy: "
        f"{metrics['test_accuracy']:.4%}"
    )

    print(
        f"Weighted Precision: "
        f"{metrics['weighted_precision']:.4%}"
    )

    print(
        f"Weighted Recall: "
        f"{metrics['weighted_recall']:.4%}"
    )

    print(
        f"Weighted F1 Score: "
        f"{metrics['weighted_f1_score']:.4%}"
    )

    print(
        f"\nEvaluation files saved in:\n"
        f"{EVALUATION_DIR}"
    )


if __name__ == "__main__":
    main()