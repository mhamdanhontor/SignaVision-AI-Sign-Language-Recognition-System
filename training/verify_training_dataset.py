from pathlib import Path

from PIL import Image

from dataset_config import (
    TRAINING_DIR,
    CLASS_NAMES,
)


VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def count_images(directory: Path) -> int:
    return sum(
        1
        for file in directory.iterdir()
        if file.is_file()
        and file.suffix.lower() in VALID_EXTENSIONS
    )


def verify_dataset():
    print("=" * 70)
    print("SignaVision - Training Dataset Verification")
    print("=" * 70)

    if not TRAINING_DIR.exists():
        print("\nERROR:")
        print(f"Training directory does not exist:\n{TRAINING_DIR}")
        return False

    print(f"\nTraining directory:")
    print(TRAINING_DIR)

    print("\n" + "-" * 70)
    print("CLASS CHECK")
    print("-" * 70)

    total_images = 0
    missing_classes = []

    for class_name in CLASS_NAMES:

        class_directory = TRAINING_DIR / class_name

        if not class_directory.exists():
            print(f"{class_name:10} -> MISSING")
            missing_classes.append(class_name)
            continue

        count = count_images(class_directory)

        total_images += count

        print(f"{class_name:10} -> {count:,} images")

    print("\n" + "-" * 70)
    print("SUMMARY")
    print("-" * 70)

    print(f"Expected classes : {len(CLASS_NAMES)}")
    print(f"Found classes    : {len(CLASS_NAMES) - len(missing_classes)}")
    print(f"Total images     : {total_images:,}")

    if missing_classes:

        print("\nMissing classes:")

        for class_name in missing_classes:
            print(f"  - {class_name}")

        return False

    print("\nAll classes are present.")

    return True


if __name__ == "__main__":
    success = verify_dataset()

    print("\n" + "=" * 70)

    if success:
        print("DATASET VERIFICATION PASSED")
    else:
        print("DATASET VERIFICATION FAILED")

    print("=" * 70)