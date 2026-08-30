# 🤟 SignaVision — AI Sign Language Recognition System

> A real-time American Sign Language (ASL) alphabet recognition system built with a custom Convolutional Neural Network (CNN), MediaPipe hand detection, React, and FastAPI.

## Overview

SignaVision is an end-to-end AI/computer-vision application that recognizes ASL alphabet-style hand gestures in real time. It combines a custom CNN classifier with MediaPipe hand detection, a React/Vite frontend, and a FastAPI prediction backend.

### Supported classes

- A–Z
- `del`
- `nothing`
- `space`

Total: **29 classes**.

## Key Features

- Custom CNN for 29-class ASL gesture classification
- 128×128×3 model input
- Real-time webcam recognition
- MediaPipe hand detection and hand-region cropping
- Prediction confidence display
- Recognition history with confidence and timestamps
- FastAPI image prediction endpoint
- React/Vite interactive frontend
- Baseline CNN comparison
- Confusion matrix and classification report
- External-image inference testing
- Automated frontend and backend tests
- Trained model packaged for Hugging Face

## Model Performance

Test set: **8,700 images**, **29 classes**.

| Metric | Custom CNN | Baseline CNN |
|---|---:|---:|
| Accuracy | **99.7241%** | 60.1954% |
| Precision | **99.7282%** | 63.2020% |
| Recall | **99.7241%** | 60.1954% |
| F1 Score | **99.7243%** | 58.7543% |
| Top-3 Accuracy | **99.9885%** | 84.2759% |

Final model test loss: **0.0097639**.

An additional external test containing 28 separately supplied images achieved **28/28 correct (100%)**. This small external test is a sanity check, not a generalization benchmark; the primary reported result is the 8,700-image held-out test set.

## Architecture

```text
Webcam
  ↓
MediaPipe Hand Detection
  ↓
Hand Region / Crop
  ↓
Image Preprocessing (128×128×3)
  ↓
Custom CNN (TensorFlow/Keras)
  ↓
29-Class Prediction
  ↓
Prediction + Confidence
  ↓
Recognition History / UI
```

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Deep Learning | TensorFlow / Keras |
| Hand Detection | MediaPipe |
| Backend | FastAPI + Uvicorn |
| Frontend | React + Vite |
| UI | Bootstrap / Bootstrap Icons |
| Testing | Pytest + Vitest |
| Model Format | Keras `.keras` |
| Model Hosting | Hugging Face |
| Version Control | Git / GitHub |

## Project Structure

```text
signavision/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── dataset/
├── docs/
│   ├── evaluation/
│   ├── external_test/
│   ├── model_comparison/
│   ├── training_results/
│   └── testing.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.*
├── models/
│   ├── metadata/
│   ├── huggingface/
│   ├── signavision_cnn_best.keras
│   └── signavision_cnn_final.keras
├── training/
├── LICENSE
├── README.md
└── run_tests.ps1
```

## Requirements

- Windows/macOS/Linux
- Python 3.11.x recommended
- Node.js and npm
- Git
- Webcam for live recognition
- Modern browser with camera permission support

## Installation

### 1. Clone

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SignaVision-AI-Sign-Language-Recognition-System
```

### 2. Python environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Backend dependencies

```powershell
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Frontend dependencies

```powershell
cd frontend
npm install
```

## Run Locally

### Backend

From the project root:

```powershell
.\venv\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

Expected health response:

```json
{
  "status": "healthy",
  "model": "SignaVision Custom CNN",
  "classes": 29
}
```

### Frontend

Open a second terminal:

```powershell
cd frontend
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

Allow camera access when prompted.

## API

The FastAPI backend exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health/model status |
| POST | `/predict` | Predict a sign from an uploaded image |

Swagger UI is available at `/docs` while the backend is running.

## Testing

From the project root:

```powershell
.\run_tests.ps1
```

The test suite covers frontend and backend functionality, including API health, model existence, model input shape, 29-class output, prediction behavior, API utilities, and hand-cropping utilities.

## Evaluation Scripts

Saved-model validation:

```powershell
python training\test_saved_model.py
```

Baseline evaluation:

```powershell
python training\evaluate_baseline.py
```

Model comparison:

```powershell
python training\compare_models.py
```

Evaluation artifacts are stored under `docs/`.

## Evaluation Artifacts

```text
docs/
├── evaluation/
│   ├── classification_report.txt
│   ├── confusion_matrix.png
│   └── metrics.json
├── external_test/
│   └── external_predictions.csv
└── model_comparison/
    ├── baseline_metrics.json
    └── model_comparison.json
```

## Hugging Face Model

The trained model and metadata are published in the project's Hugging Face repository. The model package includes the trained `.keras` model, class mapping, metadata, and an inference example.

**Hugging Face repository:** `hamdanzameer/signavision-cnn`

## Limitations

- The current system focuses on static ASL alphabet-style gestures rather than complete ASL sentence translation.
- Accuracy depends on dataset quality and distribution.
- Real-world performance can vary with lighting, camera quality, background, distance, hand orientation, and user variation.
- The 100% external result is based on only 28 images and should not be treated as a large-scale generalization result.
- Dynamic signs involving motion, facial expression, body pose, or temporal context require a temporal/dynamic recognition approach.

## Future Work

- Dynamic sign and word recognition
- Sentence-level recognition
- Larger and more diverse datasets
- Multi-hand recognition
- Stronger segmentation and background robustness
- Model quantization / TFLite / ONNX inference
- Mobile deployment
- Speech output
- More extensive real-world evaluation

## Academic Context

**Project:** SignaVision — AI Sign Language Recognition System  
**Course:** Artificial Neural Networks / AI Project  
**Semester:** 7th Semester  
**Author:** Muhammad Hamdan

The project demonstrates an end-to-end workflow from dataset preparation and CNN training through evaluation, model packaging, API development, frontend integration, testing, and real-time inference.

## Author

**Muhammad Hamdan**  
BS Artificial Intelligence

GitHub: `mhamdanhontor`

## License

This project is licensed under the MIT License. See `LICENSE` for details.

The MIT license applies to the original project code and documentation. Third-party libraries, datasets, external assets, and model components may have separate licenses or terms.

## Acknowledgments

Built with the open-source ecosystems of TensorFlow/Keras, MediaPipe, FastAPI, React, Vite, Bootstrap, Hugging Face, Pytest, and Vitest.

## ⭐ Support

If you find SignaVision useful or interesting, consider starring the GitHub repository and sharing the project with others interested in computer vision, deep learning, accessibility technology, and sign-language recognition.
