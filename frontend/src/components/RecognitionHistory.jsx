function RecognitionHistory({
  history,
  onClear,
}) {
  return (
    <div className="card shadow-sm border-0">

      <div className="card-body p-4">

        <div className="d-flex justify-content-between align-items-center mb-4">

          <div>

            <h2 className="h5 fw-bold mb-1">
              Recognition History
            </h2>

            <p className="text-secondary small mb-0">
              Recently detected signs
            </p>

          </div>


          <button
            className="btn btn-sm btn-outline-danger"
            onClick={onClear}
            disabled={!history.length}
          >
            <i className="bi bi-trash me-1"></i>
            Clear
          </button>

        </div>


        {!history.length ? (

          <div className="history-empty">

            <i className="bi bi-clock-history display-6 mb-3"></i>

            <p className="mb-0">
              No recognition history yet.
            </p>

          </div>

        ) : (

          <div className="table-responsive">

            <table className="table align-middle mb-0">

              <thead>

                <tr>

                  <th>
                    Sign
                  </th>

                  <th>
                    Confidence
                  </th>

                  <th>
                    Time
                  </th>

                </tr>

              </thead>


              <tbody>

                {history.map(
                  (item) => (

                    <tr key={item.id}>

                      <td>

                        <span className="history-sign">
                          {item.sign}
                        </span>

                      </td>


                      <td>

                        <div className="d-flex align-items-center gap-2">

                          <div
                            className="progress history-progress"
                          >

                            <div
                              className="progress-bar"
                              style={{
                                width: `${item.confidence * 100}%`,
                              }}
                            />

                          </div>

                          <span className="small fw-semibold">
                            {(
                              item.confidence *
                              100
                            ).toFixed(1)}
                            %
                          </span>

                        </div>

                      </td>


                      <td className="text-secondary small">
                        {item.time}
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        )}

      </div>

    </div>
  );
}

export default RecognitionHistory;