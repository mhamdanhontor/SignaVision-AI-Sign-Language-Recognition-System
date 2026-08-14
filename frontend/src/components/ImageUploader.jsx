import { useRef } from "react";

function ImageUploader({
  selectedFile,
  onFileSelect,
  onPredict,
  disabled,
}) {
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    onFileSelect(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    const file = event.dataTransfer.files?.[0];

    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      return;
    }

    onFileSelect(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body p-4">

        <h2 className="h5 fw-bold mb-3">
          Upload Sign Image
        </h2>

        <div
          className="upload-zone"
          onClick={() =>
            fileInputRef.current?.click()
          }
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >

          <div className="upload-icon mb-3">
            <i className="bi bi-cloud-arrow-up"></i>
          </div>

          <h3 className="h6 fw-bold">
            Drop your image here
          </h3>

          <p className="text-secondary mb-2">
            or click to browse
          </p>

          <small className="text-secondary">
            JPG, PNG or WEBP
          </small>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleFileChange}
            hidden
          />

        </div>

        {selectedFile && (
          <div className="selected-file mt-3">
            <div className="d-flex justify-content-between align-items-center">

              <div className="text-truncate">
                <i className="bi bi-image me-2"></i>
                {selectedFile.name}
              </div>

              <span className="badge bg-secondary">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </span>

            </div>
          </div>
        )}

        <button
          className="btn btn-primary w-100 mt-3"
          onClick={onPredict}
          disabled={!selectedFile || disabled}
        >
          {disabled ? (
            <>
              <span
                className="spinner-border spinner-border-sm me-2"
              ></span>

              Analysing...
            </>
          ) : (
            <>
              <i className="bi bi-cpu me-2"></i>
              Recognise Sign
            </>
          )}
        </button>

      </div>
    </div>
  );
}

export default ImageUploader;