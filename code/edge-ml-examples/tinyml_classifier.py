#!/usr/bin/env python3
"""
TinyML Biosignal Classifier
============================

Train a lightweight neural network for EMG gesture classification
suitable for deployment on microcontrollers.

Author: Jack Doyle (J9ck)
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Install with: pip install tensorflow")


def create_tinyml_model(input_shape, num_classes):
    """Create ultra-lightweight model for TinyML deployment."""
    if not TF_AVAILABLE:
        return None
    
    model = keras.Sequential([
        keras.layers.Dense(16, activation='relu', input_shape=(input_shape,)),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print(f"Model size: ~{model.count_params() * 4 / 1024:.1f} KB (float32)")
    
    return model


def convert_to_tflite(model, representative_data):
    """Convert Keras model to TensorFlow Lite with quantization."""
    if not TF_AVAILABLE:
        return None
    
    # Convert to TFLite with quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    def representative_dataset():
        for data in representative_data:
            yield [np.array([data], dtype=np.float32)]
    
    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    
    tflite_model = converter.convert()
    
    print(f"TFLite model size: {len(tflite_model) / 1024:.1f} KB (quantized)")
    
    return tflite_model


def main():
    """Demonstration of TinyML classifier training."""
    
    if not TF_AVAILABLE:
        print("Please install TensorFlow to run this example.")
        return
    
    # Generate synthetic EMG features for 3 gestures
    np.random.seed(42)
    n_samples = 300
    n_features = 8  # Time and frequency features
    n_classes = 3   # 3 gestures
    
    # Synthetic data
    X = np.random.randn(n_samples, n_features)
    y = np.random.randint(0, n_classes, n_samples)
    
    # Add class-specific patterns
    for i in range(n_classes):
        X[y == i] += i * 2
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Normalize
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Create and train model
    model = create_tinyml_model(n_features, n_classes)
    
    print("\nTraining model...")
    model.fit(X_train, y_train, epochs=50, batch_size=32, 
              validation_split=0.2, verbose=0)
    
    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nTest Accuracy: {accuracy*100:.1f}%")
    
    # Convert to TFLite
    print("\nConverting to TensorFlow Lite...")
    tflite_model = convert_to_tflite(model, X_train[:100])
    
    # Save TFLite model
    import os
    import tempfile
    output_dir = tempfile.gettempdir()
    output_path = os.path.join(output_dir, 'gesture_classifier.tflite')
    
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"\nTFLite model saved to {output_path}")
    print("Deploy this model to a microcontroller using TensorFlow Lite Micro!")


if __name__ == "__main__":
    main()
