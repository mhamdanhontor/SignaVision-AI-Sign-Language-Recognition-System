function RecognitionStats({
  currentSign,
  confidence,
  totalSigns,
  totalWords,
}) {
  return (
    <div className="row g-3">

      <div className="col-sm-6 col-lg-3">
        <div className="dashboard-stat">

          <div className="dashboard-stat-icon">
            <i className="bi bi-hand-index-thumb"></i>
          </div>

          <div className="dashboard-stat-value">
            {currentSign || "—"}
          </div>

          <div className="dashboard-stat-label">
            Current Sign
          </div>

        </div>
      </div>


      <div className="col-sm-6 col-lg-3">
        <div className="dashboard-stat">

          <div className="dashboard-stat-icon">
            <i className="bi bi-speedometer2"></i>
          </div>

          <div className="dashboard-stat-value">
            {confidence
              ? `${(
                  confidence * 100
                ).toFixed(1)}%`
              : "—"}
          </div>

          <div className="dashboard-stat-label">
            Confidence
          </div>

        </div>
      </div>


      <div className="col-sm-6 col-lg-3">
        <div className="dashboard-stat">

          <div className="dashboard-stat-icon">
            <i className="bi bi-hand-index"></i>
          </div>

          <div className="dashboard-stat-value">
            {totalSigns}
          </div>

          <div className="dashboard-stat-label">
            Signs Recognised
          </div>

        </div>
      </div>


      <div className="col-sm-6 col-lg-3">
        <div className="dashboard-stat">

          <div className="dashboard-stat-icon">
            <i className="bi bi-chat-square-text"></i>
          </div>

          <div className="dashboard-stat-value">
            {totalWords}
          </div>

          <div className="dashboard-stat-label">
            Words Formed
          </div>

        </div>
      </div>

    </div>
  );
}

export default RecognitionStats;