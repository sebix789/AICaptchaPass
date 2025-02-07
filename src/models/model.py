import tensorflow as tf
import os
import sys
from src.metrics.metricsCNN import metrics_accuracy_and_loss

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.preprocess.prepareImage import get_train_dataset, get_val_dataset, TRAIN_DIR, VAL_DIR


# Load model
def load_model():   
    model_path = 'src/models/model_after_further_training2.keras'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file {model_path} does not exist.")
    
    model = tf.keras.models.load_model(model_path)
    return model


# Build the model
def build_model():
    # Transer Learning Implementation
    base_model = tf.keras.applications.ResNet50(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False
    
    model = tf.keras.models.Sequential([
        # Base model
        base_model,
        
        # Dense layers
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(200, activation='softmax')
    ])
    
    return model


def load_data():
    train_dataset = get_train_dataset(TRAIN_DIR, batch_size=128)
    val_dataset = get_val_dataset(VAL_DIR, batch_size=128)
    
    return train_dataset, val_dataset



def fine_tunning(model, train_data, test_data):
    
    weights_file_path = 'weights.keras'
    
    base_model = model.layers[0]
    base_model.trainable = True
    
    for layer in base_model.layers[-10:]:
        layer.trainable = True
        
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Callbacks
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(weights_file_path, save_best_only=True, monitor='val_loss', mode='min')
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, min_lr=1e-7)
    
    fine_tune_history = model.fit(
        train_data, epochs=50, 
        validation_data=test_data, 
        callbacks=[early_stopping, model_checkpoint, lr_scheduler]
    )
    
    return fine_tune_history


def train_model(): 
    train_data, test_data = load_data()
    
    model_load_path = 'captcha_classification.keras'
    weights_load_path = 'weights.keras'
    
    model_file_path = 'captcha_classification.keras'
    weights_file_path = 'weights.keras'

    # Load or build the model
    if os.path.exists(model_load_path):
        print("Loading existing model...")
        model = tf.keras.models.load_model(weights_load_path)
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    else:
        print("Building new model...")
        model = build_model()

    # Load weights if they exist
    if os.path.exists(weights_file_path):
        print("Loading existing weights...")
        model.load_weights(weights_file_path)
    else:
        print("No existing weights found, starting with random initialization.")
        
    
    # Compile model
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    print("Model compiled.")
    
    # Callbacks
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(weights_file_path, save_best_only=True, monitor='val_loss', mode='min')
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, min_lr=1e-5)

    # Train the model
    history = model.fit(
        train_data, epochs=10, 
        validation_data=test_data, 
        callbacks=[early_stopping, model_checkpoint, lr_scheduler]
    )
    
    print("Fine-Tunning applying...")
    fine_tune_history = fine_tunning(model, train_data, test_data)

    model.save(model_file_path)
    
    
    for key in fine_tune_history.history:
        history.history[key] += fine_tune_history.history[key]
        
        
    return model, history, test_data
    
if __name__ == '__main__':
    model, history, test_data = train_model()
    metrics_accuracy_and_loss(history, 'accuracy.png', 'loss.png')
    
    score = model.evaluate(test_data, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])