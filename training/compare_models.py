from pathlib import Path
import json

import tensorflow as tf
import matplotlib.pyplot as plt


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

CUSTOM_METRICS = (
    PROJECT_ROOT
    / "docs"
    / "evaluation"
    / "metrics.json"
)

BASELINE_METRICS = (
    PROJECT_ROOT
    / "docs"
    / "model_comparison"
    / "baseline_metrics.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "model_comparison"
)

COMPARISON_JSON = (
    OUTPUT_DIR
    / "model_comparison.json"
)


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    custom = load_json(
        CUSTOM_METRICS
    )

    baseline = load_json(
        BASELINE_METRICS
    )

    comparison = {

        "custom_cnn": {
            "test_accuracy":
                custom["test_accuracy"],

            "precision":
                custom["weighted_precision"],

            "recall":
                custom["weighted_recall"],

            "f1_score":
                custom["weighted_f1_score"],

            "top_3_accuracy":
                custom["top_3_accuracy"],
        },

        "baseline_cnn": {
            "test_accuracy":
                baseline["test_accuracy"],

            "precision":
                baseline["weighted_precision"],

            "recall":
                baseline["weighted_recall"],

            "f1_score":
                baseline["weighted_f1_score"],

            "top_3_accuracy":
                baseline["top_3_accuracy"],
        },
    }

    # --------------------------------------------------------
    # Save comparison JSON
    # --------------------------------------------------------

    with open(
        COMPARISON_JSON,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            comparison,
            file,
            indent=4,
        )

    # --------------------------------------------------------
    # Console comparison
    # --------------------------------------------------------

    print("=" * 80)
    print("SignaVision - Model Comparison")
    print("=" * 80)

    print(
        f"\n{'Metric':<25}"
        f"{'Custom CNN':>20}"
        f"{'Baseline CNN':>20}"
    )

    print("-" * 65)

    metrics = [
        (
            "Test Accuracy",
            "test_accuracy",
        ),
        (
            "Precision",
            "precision",
        ),
        (
            "Recall",
            "recall",
        ),
        (
            "F1 Score",
            "f1_score",
        ),
        (
            "Top-3 Accuracy",
            "top_3_accuracy",
        ),
    ]

    for label, key in metrics:

        custom_value = (
            comparison[
                "custom_cnn"
            ][key]
        )

        baseline_value = (
            comparison[
                "baseline_cnn"
            ][key]
        )

        print(
            f"{label:<25}"
            f"{custom_value:>19.4%}"
            f"{baseline_value:>19.4%}"
        )

    print(
        "\nComparison saved to:"
    )

    print(
        COMPARISON_JSON
    )


if __name__ == "__main__":
    main()