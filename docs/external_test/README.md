# External Image Evaluation

This directory contains the results of evaluating the trained SignaVision CNN on a separate set of ASL sample images.

## Purpose

The external images are separate from the training, validation, and internal test datasets.

They are used to perform an additional inference check on previously unseen sample images.

## Model

- Model: SignaVision Custom CNN
- Input size: 128 × 128 RGB
- Number of classes: 29

## Results

The prediction results are stored in:

`external_predictions.csv`

The results include:

- Expected class
- Predicted class
- Prediction confidence
- Top-3 predictions
- Correct/incorrect status

## Important

The external sample set contains 28 images and does not contain the `delete` class.

Therefore, the external accuracy should not be interpreted as a replacement for the 8,700-image internal test evaluation.

The official test performance is reported using the dedicated test dataset.