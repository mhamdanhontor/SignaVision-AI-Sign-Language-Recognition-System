# SignaVision Dataset

## Current Dataset

The `raw/` directory currently contains one sample/test image for each ASL class.

### Classes

- A-Z
- nothing
- space

Total classes:

**28**

## Image Properties

- Format: JPG
- Resolution: 200 × 200
- Color: RGB
- Current images: 28
- Images per class: 1

## Important

The current images are sample/test images and are **not sufficient for CNN training**.

A larger ASL training dataset will be added in the next dataset phase.

The current images will be retained as reference/test samples.

## Directory Structure

```text
dataset/
└── raw/
    ├── A_test.jpg
    ├── B_test.jpg
    ├── ...
    ├── Z_test.jpg
    ├── nothing_test.jpg
    └── space_test.jpg


Dataset Usage

This project uses publicly available ASL image data for educational and research purposes.

The original dataset's license and attribution requirements will be documented before the training dataset is added.


---

# 2.5 Add a Dataset Visualization Script

Since we're doing this in **VS Code**, not Jupyter, we'll use Python scripts.

Create:

```text
training/visualize_dataset.py