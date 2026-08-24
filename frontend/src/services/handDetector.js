import {
  FilesetResolver,
  HandLandmarker,
} from "@mediapipe/tasks-vision";


let handLandmarker = null;


const WASM_PATH =
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.0/wasm";

const MODEL_PATH =
  "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task";


export const initializeHandDetector =
  async () => {

    if (handLandmarker) {
      return handLandmarker;
    }


    const vision =
      await FilesetResolver.forVisionTasks(
        WASM_PATH
      );


    handLandmarker =
      await HandLandmarker.createFromOptions(
        vision,
        {
          baseOptions: {
            modelAssetPath:
              MODEL_PATH,
          },

          runningMode: "VIDEO",

          numHands: 1,

          minHandDetectionConfidence:
            0.5,

          minHandPresenceConfidence:
            0.5,

          minTrackingConfidence:
            0.5,
        }
      );


    return handLandmarker;
  };


export const detectHand = (
  video,
  timestamp
) => {

  if (!handLandmarker) {
    return null;
  }


  return handLandmarker.detectForVideo(
    video,
    timestamp
  );
};


export const closeHandDetector = () => {

  if (handLandmarker) {

    handLandmarker.close();

    handLandmarker = null;
  }
};