import {
  initializeHandDetector,
  detectHand,
  closeHandDetector,
} from "../services/handDetector";

import {
  getHandBoundingBox,
  cropHandToCanvas,
} from "../utils/cropHand";


import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  predictImageBlob,
} from "../services/api";


const CONFIDENCE_THRESHOLD = 0.85;

const HISTORY_SIZE = 5;

const STABILITY_REQUIRED = 3;

const INFERENCE_INTERVAL = 800;


function WebcamRecognizer({
  onStablePrediction,
}) {

  const videoRef = useRef(null);

  const canvasRef = useRef(null);

  const streamRef = useRef(null);

  const intervalRef = useRef(null);

  const historyRef = useRef([]);

  const processingRef = useRef(false);


    const handDetectorRef =
    useRef(null);

  const lastVideoTimeRef =
    useRef(-1);
  const [handBox, setHandBox] =
  useState(null);

  const [cameraActive, setCameraActive] =
    useState(false);

  const [prediction, setPrediction] =
    useState(null);

  const [stablePrediction, setStablePrediction] =
    useState(null);

  const [error, setError] =
    useState("");

  const [processing, setProcessing] =
    useState(false);
  
  const [
  handDetected,
  setHandDetected,
  ] = useState(false);


  // ========================================================
  // Start Camera
  // ========================================================

  const startCamera = async () => {

    try {

      setError("");

      const stream =
        await navigator.mediaDevices.getUserMedia(
          {
            video: {
              width: {
                ideal: 640,
              },

              height: {
                ideal: 480,
              },

              facingMode: "user",
            },

            audio: false,
          }
        );

      streamRef.current =
        stream;

      if (videoRef.current) {

        videoRef.current.srcObject =
          stream;

        await videoRef.current.play();
      }

      historyRef.current = [];

      setPrediction(null);

      setStablePrediction(null);

      setCameraActive(true);

    } catch (err) {

      console.error(err);

      setError(
        "Unable to access your camera. " +
        "Please allow camera permission."
      );
    }
  };


  // ========================================================
  // Stop Camera
  // ========================================================

  const stopCamera = () => {

    if (intervalRef.current) {

      clearInterval(
        intervalRef.current
      );

      intervalRef.current = null;
    }

    if (streamRef.current) {

      streamRef.current
        .getTracks()
        .forEach(
          (track) => track.stop()
        );

      streamRef.current = null;
    }

    if (videoRef.current) {

      videoRef.current.srcObject =
        null;
    }

    historyRef.current = [];

    processingRef.current = false;

    setCameraActive(false);

    setPrediction(null);

    setStablePrediction(null);

    setProcessing(false);

    setHandDetected(false);

    setHandBox(null);
  };


  // ========================================================
  // Calculate Stable Prediction
  // ========================================================

  const calculateStablePrediction = (
    currentPrediction
  ) => {

    historyRef.current.push(
      currentPrediction
    );

    if (
      historyRef.current.length >
      HISTORY_SIZE
    ) {

      historyRef.current.shift();
    }


    const counts = {};

    historyRef.current.forEach(
      (item) => {

        counts[item] =
          (counts[item] || 0) + 1;

      }
    );


    let bestPrediction = null;

    let bestCount = 0;

    Object.entries(counts).forEach(
      ([className, count]) => {

        if (count > bestCount) {

          bestPrediction =
            className;

          bestCount =
            count;
        }

      }
    );


    if (
      bestCount >=
      STABILITY_REQUIRED
    ) {

      return bestPrediction;
    }

    return null;
  };


  // ========================================================
  // Capture Frame
  // ========================================================

const captureFrame = () => {

  if (
    !videoRef.current ||
    !canvasRef.current ||
    processingRef.current ||
    !handDetectorRef.current
  ) {
    return;
  }


  const video =
    videoRef.current;


  if (
    video.readyState <
    HTMLMediaElement.HAVE_CURRENT_DATA
  ) {
    return;
  }


  const currentTime =
    video.currentTime;


  if (
    currentTime ===
    lastVideoTimeRef.current
  ) {
    return;
  }


  lastVideoTimeRef.current =
    currentTime;


  try {

    // ======================================================
    // STEP 1 — Detect Hand
    // ======================================================

    const timestamp =
      performance.now();


    const result =
      detectHand(
        video,
        timestamp
      );


if (
  !result ||
  !result.landmarks ||
  !result.landmarks.length
) {
  setHandDetected(false);
  setHandBox(null);

  historyRef.current = [];

  setStablePrediction(null);

  setPrediction(null);

  return;
}

setHandDetected(true);


    // ======================================================
    // STEP 2 — Get First Hand
    // ======================================================

    const handLandmarks =
      result.landmarks[0];


    // ======================================================
    // STEP 3 — Calculate Bounding Box
    // ======================================================

    const boundingBox =
      getHandBoundingBox(
        handLandmarks,
        video.videoWidth,
        video.videoHeight
      );



    if (!boundingBox) {
      return;
    }

    setHandDetected(true);
    setHandBox(boundingBox);


    // ======================================================
    // STEP 4 — Crop Hand
    // ======================================================

    const cropped =
      cropHandToCanvas(
        video,
        canvasRef.current,
        boundingBox
      );


    if (!cropped) {
      return;
    }


    // ======================================================
    // STEP 5 — Convert Crop to Blob
    // ======================================================

    canvasRef.current.toBlob(
      async (blob) => {

        if (!blob) {
          return;
        }


        try {

          processingRef.current =
            true;

          setProcessing(true);


          // ================================================
          // STEP 6 — Send ONLY the hand crop
          // ================================================

          const result =
            await predictImageBlob(
              blob
            );


          setPrediction(
            result
          );


          // ================================================
          // STEP 7 — Confidence filtering
          // ================================================

          if (
            result.confidence <
            CONFIDENCE_THRESHOLD
          ) {

            historyRef.current = [];

            setStablePrediction(
              null
            );

            return;
          }


          // ================================================
          // STEP 8 — Temporal smoothing
          // ================================================

          const stable =
            calculateStablePrediction(
              result.prediction
            );


          if (stable) {

            setStablePrediction(
              stable
            );


            if (
              onStablePrediction
            ) {

              onStablePrediction(
                {
                  sign: stable,

                  confidence:
                    result.confidence,
                }
              );
            }
          }

        } catch (error) {

          console.error(
            "Prediction failed:",
            error
          );

          setError(
            "Prediction request failed."
          );

        } finally {

          processingRef.current =
            false;

          setProcessing(false);
        }

      },

      "image/jpeg",

      0.85
    );

  } catch (error) {

    console.error(
      "Hand detection failed:",
      error
    );

  }
};


  useEffect(() => {

  let mounted = true;


  const initialize = async () => {

    try {

      const detector =
        await initializeHandDetector();


      if (mounted) {

        handDetectorRef.current =
          detector;
           console.log(
          "MediaPipe Hand Detector ready"
        );
      }

    } catch (error) {

      console.error(
        "Hand detector initialization failed:",
        error
      );

      setError(
        "Hand detection could not be initialized."
      );
    }
  };




  initialize();


  return () => {

    mounted = false;

    closeHandDetector();

  };

}, []);


  // ========================================================
  // Prediction Loop
  // ========================================================

  useEffect(() => {

    if (!cameraActive) {
      return;
    }


    intervalRef.current =
      setInterval(
        captureFrame,
        INFERENCE_INTERVAL
      );


    return () => {

      if (intervalRef.current) {

        clearInterval(
          intervalRef.current
        );

        intervalRef.current =
          null;
      }

    };

  }, [
    cameraActive,
  ]);


  // ========================================================
  // Cleanup
  // ========================================================

  useEffect(() => {

    return () => {

      if (streamRef.current) {

        streamRef.current
          .getTracks()
          .forEach(
            (track) => track.stop()
          );
      }

    };

  }, []);


  // ========================================================
  // Render
  // ========================================================

  return (
    <div className="card shadow-sm border-0">

      <div className="card-body p-4">

        <div className="d-flex justify-content-between align-items-center mb-3">

          <div>

            <h2 className="h5 fw-bold mb-1">
              Real-Time Recognition
            </h2>

            <p className="text-secondary small mb-0">
              Show an ASL sign to the camera.
            </p>

          </div>


          {cameraActive && (

<span className="badge bg-success">

  <span className="live-dot"></span>

  LIVE

</span>

          )}

        </div>


        {error && (

          <div className="alert alert-danger">

            {error}

          </div>

        )}


        <div className="webcam-container">

          <video
            ref={videoRef}
            className="webcam-video"
            muted
            playsInline
          />

          {handBox && (
  <div
    className="hand-bounding-box"
    style={{
      left: `${
        (handBox.x /
          videoRef.current.videoWidth) *
        100
      }%`,

      top: `${
        (handBox.y /
          videoRef.current.videoHeight) *
        100
      }%`,

      width: `${
        (handBox.width /
          videoRef.current.videoWidth) *
        100
      }%`,

      height: `${
        (handBox.height /
          videoRef.current.videoHeight) *
        100
      }%`,
    }}
  >
    <span className="hand-box-label">
      Hand
    </span>
  </div>
)}


          {!cameraActive && (

            <div className="webcam-placeholder">

              <i className="bi bi-camera-video display-4 mb-3"></i>

              <div>
                Camera is off
              </div>

            </div>

          )}


          {cameraActive &&
            prediction && (

              <div className="webcam-overlay">

                <div className="overlay-prediction">

                  {stablePrediction ||
                    prediction.prediction}

                </div>


                <div className="overlay-confidence">

                  {(
                    prediction.confidence *
                    100
                  ).toFixed(1)}
                  %

                </div>

              </div>

          )}

          {cameraActive && (
            <div
              className={
                handDetected
                  ? "hand-status detected"
                  : "hand-status"
              }
            >

              <span className="hand-status-dot"></span>

              {handDetected
                ? "Hand detected"
                : "Show your hand"}

            </div>
          )}

        </div>


        <canvas
          ref={canvasRef}
          hidden
        />


        <div className="d-flex gap-2 mt-3">

          {!cameraActive ? (

            <button
              className="btn btn-primary flex-grow-1"
              onClick={startCamera}
            >

              <i className="bi bi-camera-video me-2"></i>

              Start Camera

            </button>

          ) : (

            <button
              className="btn btn-danger flex-grow-1"
              onClick={stopCamera}
            >

              <i className="bi bi-stop-circle me-2"></i>

              Stop Camera

            </button>

          )}

        </div>





        {cameraActive &&
          stablePrediction && (

            <div className="alert alert-success mt-3 mb-0">

              <i className="bi bi-check-circle me-2"></i>

              Stable sign detected:

              <strong className="ms-1">

                {stablePrediction}

              </strong>

            </div>

        )}

      </div>

    </div>
  );
}


export default WebcamRecognizer;