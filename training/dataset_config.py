from pathlib import Path


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_ROOT = PROJECT_ROOT / "dataset"

RAW_TEST_DIR = DATASET_ROOT / "raw"

TRAINING_DIR = DATASET_ROOT / "training"

PROCESSED_DIR = DATASET_ROOT / "processed"

TRAIN_DIR = PROCESSED_DIR / "train"

VALIDATION_DIR = PROCESSED_DIR / "validation"

TEST_DIR = PROCESSED_DIR / "test"


# ============================================================
# ASL Classes
# ============================================================

CLASS_NAMES = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "del",
    "nothing",
    "space",
]

NUM_CLASSES = len(CLASS_NAMES)


# ============================================================
# Image Configuration
# ============================================================

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_CHANNELS = 3

IMAGE_SIZE = (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
)


# ============================================================
# Training Configuration
# ============================================================

BATCH_SIZE = 32

RANDOM_SEED = 42


# ============================================================
# Dataset Split
# ============================================================

TRAIN_SPLIT = 0.80
VALIDATION_SPLIT = 0.10
TEST_SPLIT = 0.10


# ============================================================
# Data Augmentation Configuration
# ============================================================

ROTATION_FACTOR = 0.08

ZOOM_FACTOR = 0.10

TRANSLATION_FACTOR = 0.10

CONTRAST_FACTOR = 0.10


# ============================================================
# Performance
# ============================================================

AUTOTUNE = "AUTOTUNE"