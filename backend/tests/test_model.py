from pathlib import Path

import numpy as np
from tensorflow.keras.models import load_model


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "signavision_cnn_best.keras"
)


def test_model_exists():
    assert MODEL_PATH.exists()


def test_model_input_shape():
    model = load_model(
        MODEL_PATH,
        compile=False,
    )

    assert model.input_shape == (
        None,
        128,
        128,
        3,
    )


def test_model_output_classes():
    model = load_model(
        MODEL_PATH,
        compile=False,
    )

    assert model.output_shape[-1] == 29


def test_model_prediction():
    model = load_model(
        MODEL_PATH,
        compile=False,
    )

    sample = np.zeros(
        (1, 128, 128, 3),
        dtype=np.float32,
    )

    prediction = model.predict(
        sample,
        verbose=0,
    )

    assert prediction.shape == (
        1,
        29,
    )

    assert np.isclose(
        prediction.sum(),
        1.0,
        atol=1e-4,
    )