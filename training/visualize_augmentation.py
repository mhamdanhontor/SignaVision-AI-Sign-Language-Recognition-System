import matplotlib.pyplot as plt
import tensorflow as tf

from data_loader import load_train_dataset
from augmentation import create_augmentation_pipeline


def main():

    dataset = load_train_dataset()

    augmentation = create_augmentation_pipeline()

    images, labels = next(
        iter(dataset)
    )

    augmented_images = augmentation(
        images,
        training=True,
    )

    plt.figure(
        figsize=(12, 8)
    )

    for index in range(12):

        ax = plt.subplot(
            3,
            4,
            index + 1,
        )

        image = augmented_images[
            index
        ].numpy().astype("uint8")

        ax.imshow(image)

        ax.axis("off")

    plt.suptitle(
        "SignaVision - Augmented Training Images"
    )

    plt.tight_layout()

    plt.savefig(
        "augmentation_preview.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.show()


if __name__ == "__main__":
    main()