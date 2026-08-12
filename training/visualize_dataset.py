from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset" / "raw"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

MAX_IMAGES = 28


def get_class_name(filename: str) -> str:
    stem = Path(filename).stem

    if stem.endswith("_test"):
        return stem[:-5]

    return stem


def main():
    image_files = sorted(
        file
        for file in DATASET_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not image_files:
        print("No images found.")
        return

    image_files = image_files[:MAX_IMAGES]

    columns = 7
    rows = (len(image_files) + columns - 1) // columns

    fig, axes = plt.subplots(
        rows,
        columns,
        figsize=(14, 2.5 * rows)
    )

    # Make axes iterable even when there is only one row.
    if rows == 1:
        axes = [axes]

    axes = [axis for row in axes for axis in row]

    for index, image_file in enumerate(image_files):
        image = Image.open(image_file)

        axes[index].imshow(image)
        axes[index].set_title(get_class_name(image_file.name))
        axes[index].axis("off")

    # Hide unused axes.
    for index in range(len(image_files), len(axes)):
        axes[index].axis("off")

    plt.suptitle(
        "SignaVision - ASL Dataset Samples",
        fontsize=16
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()