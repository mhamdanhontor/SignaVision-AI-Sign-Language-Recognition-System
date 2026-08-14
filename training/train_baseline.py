from pathlib import Path
import time

import tensorflow as tf
import matplotlib.pyplot as plt

from data_loader import (
    load_train_dataset,
    load_validation_dataset,
)

from augmentation import (
    create_augmentation_pipeline,
)

from baseline_model import (
    build_baseline_cnn,
    compile_baseline_model,
)


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = (
    PROJECT_ROOT / "models"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "docs"
    / "model_comparison"
)

MODEL_PATH = (
    MODELS_DIR
    / "signavision_baseline_cnn.keras"
)


# ============================================================
# Configuration
# ============================================================

EPOCHS = 8


def create_directories():

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def plot_history(history):

    history_data = history.history

    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        history_data["accuracy"],
        label="Training Accuracy",
    )

    plt.plot(
        history_data["val_accuracy"],
        label="Validation Accuracy",
    )

    plt.title(
        "Baseline CNN - Accuracy"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR
        / "baseline_accuracy.png",
        dpi=150,
    )

    plt.close()

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        history_data["loss"],
        label="Training Loss",
    )

    plt.plot(
        history_data["val_loss"],
        label="Validation Loss",
    )

    plt.title(
        "Baseline CNN - Loss"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR
        / "baseline_loss.png",
        dpi=150,
    )

    plt.close()


def main():

    create_directories()

    print("=" * 70)
    print("SignaVision - Baseline CNN Training")
    print("=" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    print("\nLoading datasets...")

    train_dataset = (
        load_train_dataset()
    )

    validation_dataset = (
        load_validation_dataset()
    )

    # --------------------------------------------------------
    # Augmentation
    # --------------------------------------------------------

    augmentation = (
        create_augmentation_pipeline()
    )

    train_dataset = train_dataset.map(
        lambda images, labels: (
            augmentation(
                images,
                training=True,
            ),
            labels,
        ),
        num_parallel_calls=(
            tf.data.AUTOTUNE
        ),
    )

    train_dataset = train_dataset.prefetch(
        tf.data.AUTOTUNE
    )

    # --------------------------------------------------------
    # Build model
    # --------------------------------------------------------

    model = build_baseline_cnn()

    model = compile_baseline_model(
        model
    )

    print("\nBaseline model:")

    model.summary()

    # --------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------

    callbacks = [

        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(
                MODEL_PATH
            ),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=2,
            restore_best_weights=True,
            verbose=1,
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=1,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    print("\nStarting baseline training...")

    start_time = time.perf_counter()

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    training_time = (
        time.perf_counter()
        - start_time
    )

    # --------------------------------------------------------
    # Save final model
    # --------------------------------------------------------

    final_model_path = (
        MODELS_DIR
        / "signavision_baseline_cnn_final.keras"
    )

    model.save(
        final_model_path
    )

    # --------------------------------------------------------
    # Save history plots
    # --------------------------------------------------------

    plot_history(history)

    # --------------------------------------------------------
    # Calculate statistics
    # --------------------------------------------------------

    best_validation_accuracy = max(
        history.history[
            "val_accuracy"
        ]
    )

    best_epoch = (
        history.history[
            "val_accuracy"
        ].index(
            best_validation_accuracy
        )
        + 1
    )

    parameter_count = (
        model.count_params()
    )

    print("\n" + "=" * 70)
    print("BASELINE TRAINING COMPLETE")
    print("=" * 70)

    print(
        f"\nBest epoch: "
        f"{best_epoch}"
    )

    print(
        f"Best validation accuracy: "
        f"{best_validation_accuracy:.4%}"
    )

    print(
        f"Parameters: "
        f"{parameter_count:,}"
    )

    print(
        f"Training time: "
        f"{training_time / 60:.2f} minutes"
    )

    print(
        f"\nBest model:\n"
        f"{MODEL_PATH}"
    )


if __name__ == "__main__":
    main()