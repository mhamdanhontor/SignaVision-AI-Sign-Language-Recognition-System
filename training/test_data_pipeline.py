import tensorflow as tf

from data_loader import (
    load_train_dataset,
    load_validation_dataset,
    load_test_dataset,
)

from augmentation import (
    create_augmentation_pipeline,
)


def inspect_dataset(
    dataset,
    name,
):
    print("\n" + "=" * 60)
    print(f"{name} DATASET")
    print("=" * 60)

    batch_images, batch_labels = next(
        iter(dataset)
    )

    print(
        f"Image batch shape: "
        f"{batch_images.shape}"
    )

    print(
        f"Label batch shape: "
        f"{batch_labels.shape}"
    )

    print(
        f"Image data type: "
        f"{batch_images.dtype}"
    )

    print(
        f"Minimum pixel value: "
        f"{tf.reduce_min(batch_images).numpy()}"
    )

    print(
        f"Maximum pixel value: "
        f"{tf.reduce_max(batch_images).numpy()}"
    )


def main():

    print("=" * 60)
    print("SignaVision - Data Pipeline Test")
    print("=" * 60)

    print("\nLoading datasets...")

    train_dataset = load_train_dataset()

    validation_dataset = load_validation_dataset()

    test_dataset = load_test_dataset()

    inspect_dataset(
        train_dataset,
        "TRAIN",
    )

    inspect_dataset(
        validation_dataset,
        "VALIDATION",
    )

    inspect_dataset(
        test_dataset,
        "TEST",
    )

    print("\n" + "=" * 60)
    print("TESTING DATA AUGMENTATION")
    print("=" * 60)

    augmentation = create_augmentation_pipeline()

    images, labels = next(
        iter(train_dataset)
    )

    augmented_images = augmentation(
        images,
        training=True,
    )

    print(
        f"Original batch shape: "
        f"{images.shape}"
    )

    print(
        f"Augmented batch shape: "
        f"{augmented_images.shape}"
    )

    print("\nData pipeline test completed successfully.")


if __name__ == "__main__":
    main()