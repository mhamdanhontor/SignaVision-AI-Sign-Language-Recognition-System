import { useState } from "react";

import Header from "./components/Header";
import ImageUploader from "./components/ImageUploader";
import PredictionResult from "./components/PredictionResult";
import TopPredictions from "./components/TopPredictions";

import { predictSign } from "./services/api";
import WebcamRecognizer from "./components/WebcamRecognizer";
import WordBuilder from "./components/WordBuilder";

import RecognitionStats from "./components/RecognitionStats";
import RecognitionHistory from "./components/RecognitionHistory";

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

  const [stableSign, setStableSign] =
  useState(null);

const handleStablePrediction = ({
  sign,
  confidence,
}) => {

  setStableSign(
    sign
  );


  if (
    sign === "nothing"
  ) {
    return;
  }


  if (
    sign === "space"
  ) {
    return;
  }


  if (
    sign === "del"
  ) {
    return;
  }


  setCurrentConfidence(
    confidence
  );


  setTotalSigns(
    (previous) =>
      previous + 1
  );


  setHistory(
    (previous) => {

      const entry = {

        id:
          Date.now() +
          Math.random(),

        sign,

        confidence,

        time:
          new Date()
            .toLocaleTimeString(),

      };


      return [
        entry,
        ...previous,
      ].slice(0, 20);

    }
  );

};

const [history, setHistory] =
  useState([]);

const [totalSigns, setTotalSigns] =
  useState(0);
const [text, setText] =
  useState("");

const wordCount =
  text.trim()
    ? text.trim().split(/\s+/).length
    : 0;

const [
  currentConfidence,
  setCurrentConfidence,
] = useState(null);



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

        <section className="mt-5">

  <div className="text-center mb-4">

    <h2 className="fw-bold">
      Real-Time ASL Recognition
    </h2>

    <p className="text-secondary">
      Use your webcam to recognise signs
      instantly.
    </p>

  </div>

  <div className="row">

    <div className="col-lg-8 mx-auto">

     <WebcamRecognizer
  onStablePrediction={
    handleStablePrediction
  }
/>

<div className="mt-4">

  <WordBuilder
    stableSign={stableSign}
    text={text}
    setText={setText}
  />

</div>
<section className="mt-5">

  <div className="mb-4">

    <h2 className="fw-bold">
      Recognition Dashboard
    </h2>

    <p className="text-secondary">
      Real-time statistics from your
      SignaVision session.
    </p>

  </div>


<RecognitionStats
  currentSign={stableSign}
  confidence={currentConfidence}
  totalSigns={totalSigns}
  totalWords={wordCount}
/>

  <section className="mt-4">

  <RecognitionHistory
    history={history}
    onClear={() =>
      setHistory([])
    }
  />

</section>

</section>

{stableSign && (
  <div className="alert alert-primary mt-3 text-center">

    <span className="text-secondary">
      Current stable sign:
    </span>

    <strong className="ms-2 fs-4">
      {stableSign}
    </strong>

  </div>
)}

    </div>

  </div>

</section>

      </main>

    </div>
  );
}

export default App;