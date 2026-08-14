import { useState } from "react";

import Header from "./components/Header";
import ImageUploader from "./components/ImageUploader";
import PredictionResult from "./components/PredictionResult";
import TopPredictions from "./components/TopPredictions";

import { predictSign } from "./services/api";


function App() {
  const [selectedFile, setSelectedFile] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
    setError("");
  };


  const handlePredict = async () => {
    if (!selectedFile) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const prediction =
        await predictSign(
          selectedFile
        );

      setResult(prediction);

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to connect to the SignaVision API."
      );

    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="app">

      <Header />

      <main className="container py-5">

        <div className="text-center mb-5">

          <span className="badge bg-primary-subtle text-primary mb-3">
            Artificial Neural Networks Project
          </span>

          <h1 className="display-5 fw-bold">
            American Sign Language
            <br />
            Recognition
          </h1>

          <p className="lead text-secondary mx-auto hero-description">
            Upload an ASL alphabet sign and let
            our custom convolutional neural
            network recognise it.
          </p>

        </div>


        {error && (
          <div className="alert alert-danger mb-4">
            <i className="bi bi-exclamation-triangle me-2"></i>
            {error}
          </div>
        )}


        <div className="row g-4">

          <div className="col-lg-6">

            <ImageUploader
              selectedFile={selectedFile}
              onFileSelect={handleFileSelect}
              onPredict={handlePredict}
              disabled={loading}
            />

          </div>


          <div className="col-lg-6">

            <PredictionResult
              result={result}
            />

          </div>

        </div>


        <div className="row">

          <div className="col-lg-6 offset-lg-6">

            <TopPredictions
              predictions={result?.top_3}
            />

          </div>

        </div>


        <section className="stats-section mt-5">

          <div className="row g-3">

            <div className="col-md-3">
              <div className="stat-card">
                <div className="stat-value">
                  29
                </div>
                <div className="stat-label">
                  Classes
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div className="stat-card">
                <div className="stat-value">
                  99.72%
                </div>
                <div className="stat-label">
                  Test Accuracy
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div className="stat-card">
                <div className="stat-value">
                  100%
                </div>
                <div className="stat-label">
                  External Test
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div className="stat-card">
                <div className="stat-value">
                  CNN
                </div>
                <div className="stat-label">
                  Architecture
                </div>
              </div>
            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;