from pydantic import BaseModel


class TopPrediction(BaseModel):

    class_name: str
    confidence: float


class PredictionResponse(BaseModel):

    prediction: str
    confidence: float
    top_3: list[dict]