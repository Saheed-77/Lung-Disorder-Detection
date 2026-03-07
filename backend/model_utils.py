"""
Model training and utilities for Hybrid MobileNet + Vision Transformer
This module contains functions for training the lung disorder detection model
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class PatchExtractor(layers.Layer):
    """Extract patches from images for Vision Transformer"""
    def __init__(self, patch_size):
        super().__init__()
        self.patch_size = patch_size

    def call(self, images):
        batch_size = tf.shape(images)[0]
        patches = tf.image.extract_patches(
            images=images,
            sizes=[1, self.patch_size, self.patch_size, 1],
            strides=[1, self.patch_size, self.patch_size, 1],
            rates=[1, 1, 1, 1],
            padding="VALID",
        )
        patch_dims = patches.shape[-1]
        patches = tf.reshape(patches, [batch_size, -1, patch_dims])
        return patches

class PatchEncoder(layers.Layer):
    """Encode patches with position embeddings"""
    def __init__(self, num_patches, projection_dim):
        super().__init__()
        self.num_patches = num_patches
        self.projection = layers.Dense(units=projection_dim)
        self.position_embedding = layers.Embedding(
            input_dim=num_patches, output_dim=projection_dim
        )

    def call(self, patch):
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        encoded = self.projection(patch) + self.position_embedding(positions)
        return encoded

def create_mobilenet_base(input_shape=(224, 224, 3)):
    """Create MobileNetV2 base for feature extraction"""
    base_model = keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    # Freeze early layers
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    return base_model

def transformer_encoder(encoded_patches, num_heads=4, transformer_units=[128, 64]):
    """Transformer encoder block"""
    # Layer normalization 1
    x1 = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
    
    # Multi-head attention
    attention_output = layers.MultiHeadAttention(
        num_heads=num_heads, 
        key_dim=transformer_units[0] // num_heads,
        dropout=0.1
    )(x1, x1)
    
    # Skip connection 1
    x2 = layers.Add()([attention_output, encoded_patches])
    
    # Layer normalization 2
    x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
    
    # MLP
    x3 = layers.Dense(transformer_units[0], activation="gelu")(x3)
    x3 = layers.Dropout(0.1)(x3)
    x3 = layers.Dense(transformer_units[1], activation="gelu")(x3)
    x3 = layers.Dropout(0.1)(x3)
    
    # Skip connection 2
    encoded_patches = layers.Add()([x3, x2])
    
    return encoded_patches

def create_hybrid_model(
    input_shape=(224, 224, 3),
    num_classes=4,
    patch_size=16,
    num_patches=64,
    projection_dim=128,
    num_heads=4,
    transformer_layers=4,
    mlp_head_units=[512, 256]
):
    """
    Create Hybrid MobileNet + Vision Transformer model
    
    Args:
        input_shape: Input image shape
        num_classes: Number of output classes
        patch_size: Size of image patches for ViT
        num_patches: Number of patches
        projection_dim: Projection dimension for patches
        num_heads: Number of attention heads
        transformer_layers: Number of transformer blocks
        mlp_head_units: MLP head layer sizes
    
    Returns:
        Keras model
    """
    inputs = layers.Input(shape=input_shape)
    
    # MobileNet feature extraction
    mobilenet_base = create_mobilenet_base(input_shape)
    cnn_features = mobilenet_base(inputs)
    
    # Global average pooling for CNN features
    cnn_output = layers.GlobalAveragePooling2D()(cnn_features)
    
    # Vision Transformer path
    # Extract patches
    patches = PatchExtractor(patch_size)(inputs)
    
    # Encode patches
    encoded_patches = PatchEncoder(num_patches, projection_dim)(patches)
    
    # Transformer encoder blocks
    for _ in range(transformer_layers):
        encoded_patches = transformer_encoder(
            encoded_patches, 
            num_heads=num_heads,
            transformer_units=[projection_dim, projection_dim // 2]
        )
    
    # Global average pooling for transformer output
    vit_output = layers.GlobalAveragePooling1D()(encoded_patches)
    
    # Fusion of CNN and Transformer features
    fused_features = layers.Concatenate()([cnn_output, vit_output])
    
    # MLP head
    x = layers.Dense(mlp_head_units[0], activation="relu")(fused_features)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(mlp_head_units[1], activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    return model

def compile_model(model, learning_rate=0.001):
    """Compile the model with optimizer and loss"""
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy', 
                 keras.metrics.Precision(name='precision'),
                 keras.metrics.Recall(name='recall'),
                 keras.metrics.AUC(name='auc')]
    )
    return model

def get_callbacks(model_path='models/best_model.h5'):
    """Get training callbacks"""
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            model_path,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    return callbacks

def preprocess_dataset(image_path, label, img_size=(224, 224)):
    """Preprocess images for training"""
    # Read image
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    
    # Resize
    image = tf.image.resize(image, img_size)
    
    # Normalize
    image = image / 255.0
    
    return image, label

if __name__ == "__main__":
    # Example usage
    print("Creating Hybrid MobileNet + ViT model...")
    model = create_hybrid_model(
        input_shape=(224, 224, 3),
        num_classes=4,
        patch_size=16,
        num_patches=64,
        projection_dim=128
    )
    
    model = compile_model(model)
    
    print("\nModel Summary:")
    model.summary()
    
    print(f"\nTotal parameters: {model.count_params():,}")
    print("\nModel architecture created successfully!")
    print("\nTo train the model, prepare your dataset and use model.fit()")
