from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.core.config import (
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
)

from app.services.predictor import (
    SignaVisionPredictor,
)


# ============================================================
# Application
# ============================================================

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Model
# ============================================================

predictor = (
    SignaVisionPredictor()
)


# ============================================================
# Health
# ============================================================

@app.get("/")
def root():

    return {
        "name": "SignaVision AI API",
        "version": API_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "SignaVision Custom CNN",
        "classes": 29,
    }


# ============================================================
# Prediction
# ============================================================

@app.post(
    "/predict"
)
async def predict(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate content type
    # --------------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, PNG or WEBP."
            ),
        )

    # --------------------------------------------------------
    # Read image
    # --------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    try:

        result = predictor.predict(
            image_bytes
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction failed: "
                f"{str(error)}"
            ),
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "filename": file.filename,
        "prediction": result[
            "prediction"
        ],
        "confidence": result[
            "confidence"
        ],
        "top_3": result[
            "top_3"
        ],
    }