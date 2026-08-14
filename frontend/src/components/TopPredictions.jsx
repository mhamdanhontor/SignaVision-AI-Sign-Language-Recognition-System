function TopPredictions({ predictions }) {
  if (!predictions?.length) {
    return null;
  }

  return (
    <div className="card shadow-sm border-0 mt-4">
      <div className="card-body p-4">

        <h2 className="h5 fw-bold mb-3">
          Top 3 Predictions
        </h2>

        <div className="list-group">

          {predictions.map(
            (item, index) => (
              <div
                key={`${item.class}-${index}`}
                className="list-group-item border-0 px-0"
              >

                <div className="d-flex align-items-center">

                  <div className="rank-circle me-3">
                    {index + 1}
                  </div>

                  <div className="flex-grow-1">

                    <div className="d-flex justify-content-between">

                      <span className="fw-semibold">
                        {item.class}
                      </span>

                      <span>
                        {(
                          item.confidence * 100
                        ).toFixed(2)}
                        %
                      </span>

                    </div>

                    <div className="progress mt-2">
                      <div
                        className="progress-bar"
                        style={{
                          width: `${
                            item.confidence * 100
                          }%`,
                        }}
                      />
                    </div>

                  </div>

                </div>

              </div>
            )
          )}

        </div>

      </div>
    </div>
  );
}

export default TopPredictions;