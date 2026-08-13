import random
import shutil
from pathlib import Path

from dataset_config import (
    TRAINING_DIR,
    PROCESSED_DIR,
    CLASS_NAMES,
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
    RANDOM_SEED,
)


VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def get_images(directory: Path):
    return [
        file
        for file in directory.iterdir()
        if file.is_file()
        and file.suffix.lower() in VALID_EXTENSIONS
    ]


def create_directories():
    for split in ["train", "validation", "test"]:

        for class_name in CLASS_NAMES:

            directory = (
                PROCESSED_DIR
                / split
                / class_name
            )

            directory.mkdir(
                parents=True,
                exist_ok=True
            )


def split_class_images(class_name: str):

    source_directory = TRAINING_DIR / class_name

    images = get_images(source_directory)

    random.shuffle(images)

    total = len(images)

    train_end = int(total * TRAIN_SPLIT)

    validation_end = train_end + int(
        total * VALIDATION_SPLIT
    )

    train_images = images[:train_end]

    validation_images = images[
        train_end:validation_end
    ]

    test_images = images[
        validation_end:
    ]

    return (
        train_images,
        validation_images,
        test_images,
    )


def copy_images(
    images,
    destination: Path
):

    for image in images:

        destination_file = (
            destination / image.name
        )

        shutil.copy2(
            image,
            destination_file
        )


def prepare_dataset():

    print("=" * 70)
    print("SignaVision - Dataset Preparation")
    print("=" * 70)

    if not TRAINING_DIR.exists():

        raise FileNotFoundError(
            f"Training dataset not found:\n{TRAINING_DIR}"
        )

    print("\nCreating processed dataset directories...")

    create_directories()

    total_train = 0
    total_validation = 0
    total_test = 0

    for class_name in CLASS_NAMES:

        print(
            f"\nProcessing class: {class_name}"
        )

        (
            train_images,
            validation_images,
            test_images,
        ) = split_class_images(class_name)

        train_destination = (
            PROCESSED_DIR
            / "train"
            / class_name
        )

        validation_destination = (
            PROCESSED_DIR
            / "validation"
            / class_name
        )

        test_destination = (
            PROCESSED_DIR
            / "test"
            / class_name
        )

        copy_images(
            train_images,
            train_destination
        )

        copy_images(
            validation_images,
            validation_destination
        )

        copy_images(
            test_images,
            test_destination
        )

        total_train += len(train_images)

        total_validation += len(
            validation_images
        )

        total_test += len(test_images)

        print(
            f"  Train      : {len(train_images):,}"
        )

        print(
            f"  Validation : {len(validation_images):,}"
        )

        print(
            f"  Test       : {len(test_images):,}"
        )

    print("\n" + "=" * 70)
    print("DATASET PREPARATION COMPLETE")
    print("=" * 70)

    print(
        f"\nTraining images   : {total_train:,}"
    )

    print(
        f"Validation images: {total_validation:,}"
    )

    print(
        f"Test images      : {total_test:,}"
    )

    print(
        f"Total images     : "
        f"{total_train + total_validation + total_test:,}"
    )

    print(
        f"\nOutput directory:\n{PROCESSED_DIR}"
    )


if __name__ == "__main__":

    random.seed(RANDOM_SEED)

    prepare_dataset()