from pathlib import Path


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)


# ============================================================
# Hugging Face
# ============================================================

HF_REPO_ID = (
    "hamdanzameer/signavision-cnn"
)

HF_MODEL_FILENAME = (
    "signavision_cnn_best.keras"
)

HF_CLASS_NAMES_FILENAME = (
    "class_names.json"
)


# ============================================================
# Model Configuration
# ============================================================

IMAGE_SIZE = (
    128,
    128,
)

NUM_CLASSES = 29

MODEL_NAME = (
    "SignaVision Custom CNN"
)


# ============================================================
# API Configuration
# ============================================================

API_TITLE = (
    "SignaVision AI API"
)

API_VERSION = "1.0.0"

API_DESCRIPTION = (
    "AI-powered American Sign Language "
    "alphabet recognition API using a "
    "custom convolutional neural network."
)