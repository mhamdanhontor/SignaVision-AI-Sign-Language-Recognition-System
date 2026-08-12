from pathlib import Path
from PIL import Image
from collections import Counter

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset" / "raw"

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

EXPECTED_CLASSES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + [
    "nothing",
    "space",
]


def get_class_name(filename: str) -> str:
    """
    Convert filenames such as:
        A_test.jpg       -> A
        B_test.jpg       -> B
        nothing_test.jpg -> nothing
        space_test.jpg   -> space
    """
    stem = Path(filename).stem

    if stem.endswith("_test"):
        return stem[:-5]

    return stem


def inspect_dataset():
    print("=" * 60)
    print("SignaVision - ASL Dataset Inspection")
    print("=" * 60)

    if not DATASET_DIR.exists():
        print(f"\nERROR: Dataset directory not found:")
        print(DATASET_DIR)
        return

    image_files = sorted(
        file
        for file in DATASET_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS
    )

    print(f"\nDataset directory:")
    print(DATASET_DIR)

    print(f"\nTotal image files: {len(image_files)}")

    if not image_files:
        print("\nERROR: No image files found.")
        return

    print("\n" + "-" * 60)
    print("IMAGE INFORMATION")
    print("-" * 60)

    class_names = []
    valid_images = 0
    corrupted_images = []

    dimensions = Counter()

    for image_file in image_files:
        class_name = get_class_name(image_file.name)
        class_names.append(class_name)

        try:
            with Image.open(image_file) as image:
                image.verify()

            # Open again after verify() because verify() invalidates the file object.
            with Image.open(image_file) as image:
                dimensions[image.size] += 1

            valid_images += 1

        except Exception as error:
            corrupted_images.append(
                {
                    "file": image_file.name,
                    "error": str(error),
                }
            )

    unique_classes = sorted(set(class_names))

    print(f"Valid images: {valid_images}")
    print(f"Corrupted images: {len(corrupted_images)}")
    print(f"Detected classes: {len(unique_classes)}")

    print("\nClasses:")
    for class_name in unique_classes:
        print(f"  - {class_name}")

    print("\n" + "-" * 60)
    print("IMAGE DIMENSIONS")
    print("-" * 60)

    for dimension, count in dimensions.items():
        print(f"{dimension[0]} x {dimension[1]} : {count} image(s)")

    print("\n" + "-" * 60)
    print("EXPECTED CLASS CHECK")
    print("-" * 60)

    missing_classes = sorted(set(EXPECTED_CLASSES) - set(unique_classes))
    unexpected_classes = sorted(set(unique_classes) - set(EXPECTED_CLASSES))

    if missing_classes:
        print("Missing classes:")
        for class_name in missing_classes:
            print(f"  - {class_name}")
    else:
        print("All expected ASL classes are present.")

    if unexpected_classes:
        print("\nUnexpected classes:")
        for class_name in unexpected_classes:
            print(f"  - {class_name}")
    else:
        print("No unexpected classes found.")

    print("\n" + "-" * 60)
    print("CORRUPTED IMAGE CHECK")
    print("-" * 60)

    if corrupted_images:
        for item in corrupted_images:
            print(f"{item['file']}: {item['error']}")
    else:
        print("No corrupted images detected.")

    print("\n" + "=" * 60)
    print("DATASET INSPECTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    inspect_dataset()