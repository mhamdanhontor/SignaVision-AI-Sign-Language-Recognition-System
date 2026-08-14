function PredictionResult({ result }) {
  if (!result) {
    return (
      <div className="card shadow-sm border-0 h-100">
        <div className="card-body d-flex flex-column justify-content-center align-items-center text-center p-5">

          <div className="result-placeholder mb-3">
            <i className="bi bi-hand-index-thumb"></i>
          </div>

          <h2 className="h5 fw-bold">
            No Prediction Yet
          </h2>

          <p className="text-secondary mb-0">
            Upload an ASL sign image to see
            the model prediction.
          </p>

        </div>
      </div>
    );
  }

  return (
    <div className="card shadow-sm border-0 h-100">
      <div className="card-body p-4">

        <div className="d-flex justify-content-between align-items-center mb-4">

          <h2 className="h5 fw-bold mb-0">
            Recognition Result
          </h2>

          <span className="badge bg-success">
            AI Prediction
          </span>

        </div>

        <div className="prediction-letter">
          {result.prediction === "nothing"
            ? "—"
            : result.prediction === "space"
            ? "␠"
            : result.prediction}
        </div>

        <div className="text-center mb-4">

          <div className="h5 fw-bold">
            {result.prediction}
          </div>

          <div className="text-secondary">
            Predicted Sign
          </div>

        </div>

        <div className="confidence-section">

          <div className="d-flex justify-content-between mb-2">

            <span className="fw-semibold">
              Confidence
            </span>

            <span className="fw-bold">
              {(result.confidence * 100).toFixed(2)}%
            </span>

          </div>

          <div className="progress">
            <div
              className="progress-bar"
              role="progressbar"
              style={{
                width: `${result.confidence * 100}%`,
              }}
            />
          </div>

        </div>

        <div className="mt-4">

          <h3 className="h6 fw-bold">
            File
          </h3>

          <div className="text-secondary small">
            {result.filename}
          </div>

        </div>

      </div>
    </div>
  );
}

export default PredictionResult;