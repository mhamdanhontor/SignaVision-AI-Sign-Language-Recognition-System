from fastapi import FastAPI

app = FastAPI(
    title="SignaVision API",
    description="AI-powered ASL Sign Language Recognition API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "SignaVision",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }