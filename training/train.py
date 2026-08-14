from pathlib import Path

import tensorflow as tf
import matplotlib.pyplot as plt

from dataset_config import (
    PROCESSED_DIR,
    CLASS_NAMES,
)

from data_loader import (
    load_train_dataset,
    load_validation_dataset,
)

from augmentation import (
    create_augmentation_pipeline,
)

from model import (
    build_cnn,
    compile_model,
)


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "training_results"

BEST_MODEL_PATH = (
    MODELS_DIR /
    "signavision_cnn_best.keras"
)


# ============================================================
# Training Configuration
# ============================================================

EPOCHS = 15


def create_directories():

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def plot_training_history(history):

    history_data = history.history

    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        history_data["accuracy"],
        label="Training Accuracy",
    )

    plt.plot(
        history_data["val_accuracy"],
        label="Validation Accuracy",
    )

    plt.title(
        "SignaVision CNN - Accuracy"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Accuracy")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "accuracy.png",
        dpi=150,
    )

    plt.close()

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        history_data["loss"],
        label="Training Loss",
    )

    plt.plot(
        history_data["val_loss"],
        label="Validation Loss",
    )

    plt.title(
        "SignaVision CNN - Loss"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Loss")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "loss.png",
        dpi=150,
    )

    plt.close()


def train():

    create_directories()

    print("=" * 70)
    print("SignaVision - CNN Training")
    print("=" * 70)

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    print("\nLoading training dataset...")

    train_dataset = load_train_dataset()

    print("\nLoading validation dataset...")

    validation_dataset = load_validation_dataset()

    # --------------------------------------------------------
    # Data augmentation
    # --------------------------------------------------------

    augmentation = (
        create_augmentation_pipeline()
    )

    # Apply augmentation only to training data.
    train_dataset = train_dataset.map(
        lambda images, labels: (
            augmentation(
                images,
                training=True,
            ),
            labels,
        ),
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    train_dataset = train_dataset.prefetch(
        tf.data.AUTOTUNE
    )

    # --------------------------------------------------------
    # Build model
    # --------------------------------------------------------

    print("\nBuilding CNN...")

    model = build_cnn()

    model = compile_model(model)

    print("\nModel created successfully.")

    model.summary()

    # --------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------

    callbacks = [

        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(
                BEST_MODEL_PATH
            ),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=3,
            restore_best_weights=True,
            verbose=1,
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("STARTING TRAINING")
    print("=" * 70)

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    # --------------------------------------------------------
    # Save final training model
    # --------------------------------------------------------

    final_model_path = (
        MODELS_DIR /
        "signavision_cnn_final.keras"
    )

    model.save(
        final_model_path
    )

    # --------------------------------------------------------
    # Save training graphs
    # --------------------------------------------------------

    plot_training_history(
        history
    )

    # --------------------------------------------------------
    # Training summary
    # --------------------------------------------------------

    best_epoch = (
        max(
            range(
                len(
                    history.history[
                        "val_accuracy"
                    ]
                )
            ),
            key=lambda index:
                history.history[
                    "val_accuracy"
                ][index],
        )
        + 1
    )

    best_accuracy = max(
        history.history[
            "val_accuracy"
        ]
    )

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    print(
        f"\nBest epoch: {best_epoch}"
    )

    print(
        f"Best validation accuracy: "
        f"{best_accuracy:.4f}"
    )

    print(
        f"\nBest model saved to:\n"
        f"{BEST_MODEL_PATH}"
    )

    print(
        f"\nFinal model saved to:\n"
        f"{final_model_path}"
    )

    print(
        f"\nTraining graphs saved to:\n"
        f"{OUTPUT_DIR}"
    )


if __name__ == "__main__":
    train()