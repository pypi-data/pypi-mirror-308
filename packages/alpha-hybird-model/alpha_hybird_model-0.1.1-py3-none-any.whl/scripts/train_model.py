import argparse
import os
from alpha_hybird_model import build_model  # Import your model from the package
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

def main():
    parser = argparse.ArgumentParser(description="Train the Alpha Hybrid Model")
    parser.add_argument("--train_dir", type=str, required=True, help="Training directory path")
    parser.add_argument("--val_dir", type=str, required=True, help="Validation directory path")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    parser.add_argument("--initial_lr", type=float, default=1e-4, help="Initial learning rate")
    parser.add_argument("--output_dir", type=str, default="./", help="Output directory for saving model weights")
    args = parser.parse_args()

    # Call to your model build function
    model = build_model()

    # Compile the model before training
    model.compile(
        optimizer=Adam(learning_rate=args.initial_lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()
    # Implement data generators with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        args.train_dir,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=True
    )
    val_generator = val_datagen.flow_from_directory(
        args.val_dir,
        target_size=(224, 224),
        batch_size=args.batch_size,
        class_mode='categorical',
        shuffle=False
    )

    # Callbacks for early stopping and learning rate reduction
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    lr_reduction = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )

    # Training the model
    history = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=val_generator,
        callbacks=[early_stopping, lr_reduction],
        verbose=1
    )

    # Save the trained model weights
    os.makedirs(args.output_dir, exist_ok=True)
    model.save_weights(os.path.join(args.output_dir, "model_weights.h5"))
    print(f"Model weights saved to {os.path.join(args.output_dir, 'model_weights.h5')}")

if __name__ == "__main__":
    main()
