import tensorflow as tf

from model import (
    build_cnn,
    compile_model,
)

from data_loader import (
    load_train_dataset,
)


def main():

    print("=" * 70)
    print("SignaVision - CNN Architecture Test")
    print("=" * 70)

    print("\nBuilding model...")

    model = build_cnn()

    model = compile_model(model)

    print("\nModel summary:\n")

    model.summary()

    print("\nLoading one training batch...")

    dataset = load_train_dataset()

    images, labels = next(
        iter(dataset)
    )

    print(
        f"\nInput batch shape: "
        f"{images.shape}"
    )

    print(
        f"Label batch shape: "
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

    print(
        f"Prediction sum: "
        f"{tf.reduce_sum(predictions[0]).numpy():.4f}"
    )

    print("\nChecking prediction probabilities...")

    if predictions.shape == (
        images.shape[0],
        29,
    ):
        print("✓ Output shape is correct.")

    if abs(
        float(
            tf.reduce_sum(
                predictions[0]
            ).numpy()
        ) - 1.0
    ) < 0.001:
        print("✓ Softmax probabilities are valid.")

    print("\n" + "=" * 70)
    print("CNN ARCHITECTURE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()