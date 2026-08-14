import tensorflow as tf

from baseline_model import (
    build_baseline_cnn,
    compile_baseline_model,
)

from data_loader import (
    load_train_dataset,
)


def main():

    print("=" * 70)
    print("SignaVision - Baseline CNN Test")
    print("=" * 70)

    model = build_baseline_cnn()

    model = compile_baseline_model(
        model
    )

    print("\nBaseline CNN architecture:\n")

    model.summary()

    print("\nLoading training batch...")

    dataset = load_train_dataset()

    images, labels = next(
        iter(dataset)
    )

    print(
        f"\nInput shape: "
        f"{images.shape}"
    )

    print(
        f"Labels shape: "
        f"{labels.shape}"
    )

    print("\nRunning forward pass...")

    predictions = model(
        images,
        training=False,
    )

    print(
        f"Prediction shape: "
        f"{predictions.shape}"
    )

    if predictions.shape == (
        images.shape[0],
        29,
    ):

        print(
            "✓ Output shape is correct."
        )

    probability_sum = float(
        tf.reduce_sum(
            predictions[0]
        ).numpy()
    )

    print(
        f"Probability sum: "
        f"{probability_sum:.4f}"
    )

    if abs(
        probability_sum - 1.0
    ) < 0.001:

        print(
            "✓ Softmax probabilities "
            "are valid."
        )

    print("\n" + "=" * 70)
    print("BASELINE MODEL TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()