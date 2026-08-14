function Header() {
  return (
    <header className="app-header">
      <div className="container">
        <div className="d-flex justify-content-between align-items-center py-3">
          
          <div>
            <h1 className="h3 mb-0 fw-bold">
              SignaVision
            </h1>

            <small className="text-secondary">
              AI-Powered ASL Recognition
            </small>
          </div>

          <div className="d-none d-md-flex align-items-center gap-2">
            <span className="badge bg-success">
              CNN
            </span>

            <span className="badge bg-dark">
              99.72% Test Accuracy
            </span>
          </div>

        </div>
      </div>
    </header>
  );
}

export default Header;