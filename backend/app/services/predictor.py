import io
import json

import numpy as np
import tensorflow as tf

from PIL import Image

from huggingface_hub import (
    hf_hub_download,
)

from app.core.config import (
    HF_REPO_ID,
    HF_MODEL_FILENAME,
    HF_CLASS_NAMES_FILENAME,
    IMAGE_SIZE,
)


class SignaVisionPredictor:

    def __init__(self):

        self.model = None
        self.class_names = None

        self._load_model()
        self._load_class_names()

    # ========================================================
    # Model Loading
    # ========================================================

    def _load_model(self):

        print(
            "Loading SignaVision model..."
        )

        model_path = (
            hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=HF_MODEL_FILENAME,
            )
        )

        self.model = (
            tf.keras.models.load_model(
                model_path
            )
        )

        print(
            "SignaVision model loaded."
        )

    # ========================================================
    # Class Loading
    # ========================================================

    def _load_class_names(self):

        print(
            "Loading class names..."
        )

        class_names_path = (
            hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=HF_CLASS_NAMES_FILENAME,
            )
        )

        with open(
            class_names_path,
            "r",
            encoding="utf-8",
        ) as file:

            mapping = json.load(file)

        self.class_names = [
            mapping[str(index)]
            for index in range(
                len(mapping)
            )
        ]

        print(
            f"Loaded "
            f"{len(self.class_names)} classes."
        )

    # ========================================================
    # Image Preprocessing
    # ========================================================

    @staticmethod
    def preprocess_image(
        image_bytes: bytes,
    ):

        image = Image.open(
            io.BytesIO(
                image_bytes
            )
        ).convert("RGB")

        image = image.resize(
            IMAGE_SIZE
        )

        image_array = np.array(
            image,
            dtype=np.float32,
        )

        image_array = np.expand_dims(
            image_array,
            axis=0,
        )

        return image_array

    # ========================================================
    # Prediction
    # ========================================================

    def predict(
        self,
        image_bytes: bytes,
    ):

        image = (
            self.preprocess_image(
                image_bytes
            )
        )

        probabilities = (
            self.model.predict(
                image,
                verbose=0,
            )[0]
        )

        predicted_index = int(
            np.argmax(
                probabilities
            )
        )

        predicted_class = (
            self.class_names[
                predicted_index
            ]
        )

        confidence = float(
            probabilities[
                predicted_index
            ]
        )

        # ----------------------------------------------------
        # Top 3
        # ----------------------------------------------------

        top_indices = np.argsort(
            probabilities
        )[-3:][::-1]

        top_predictions = []

        for index in top_indices:

            top_predictions.append(
                {
                    "class": (
                        self.class_names[
                            int(index)
                        ]
                    ),
                    "confidence": float(
                        probabilities[
                            index
                        ]
                    ),
                }
            )

        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "top_3": top_predictions,
        }