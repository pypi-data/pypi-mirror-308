
# ANN function
def first():
    print("""# Simple Perceptron Example

# Step function to make decisions (activation function)
def step_function(value):
    return 1 if value >= 0 else 0

# Perceptron learning algorithm
def perceptron(X, y, learning_rate, n_iters):
    weights = [0, 0]  # Initialize weights for two features
    bias = 0          # Initialize bias

    # Training loop
    for _ in range(n_iters):
        for i in range(len(X)):
            # Calculate weighted sum
            weighted_sum = X[i][0] * weights[0] + X[i][1] * weights[1] + bias
            prediction = step_function(weighted_sum)

            # Update rule
            error = y[i] - prediction
            weights[0] += learning_rate * error * X[i][0]
            weights[1] += learning_rate * error * X[i][1]
            bias += learning_rate * error

    return weights, bias

# Training data: AND gate logic
X = [[0, 0], [0, 1], [1, 0], [1, 1]]  # Input features
y = [0, 0, 0, 1]  # Expected output (AND gate)

# Train the perceptron
learning_rate = 0.1
n_iters = 10
weights, bias = perceptron(X, y, learning_rate, n_iters)

# Predict for a new input
def predict(X, weights, bias):
    weighted_sum = X[0] * weights[0] + X[1] * weights[1] + bias
    return step_function(weighted_sum)

# Test the perceptron
test_input = [0, 1]
print("Prediction for input [1, 1]:", predict(test_input, weights, bias))""")
    


# Bayesian Network function
def second():
    print("""import numpy as np

# Inputs and step function
INPUTS = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])

def step_function(sum): return 1 if sum >= 0 else -1

def calculate_output(weights, instance, bias): return step_function(np.dot(instance, weights) + bias)

# Hebbian Learning Algorithm
def hebb(outputs):
    weights, bias = np.zeros(2), 0  # Initialize weights and bias
    for i in range(len(outputs)):
        weights += INPUTS[i] * outputs[i]
        bias += outputs[i]
    return weights, bias

# Train, test, and print results for both AND and OR gates
def train_and_print(gate_name, outputs):
    weights, bias = hebb(outputs)
    print(f"\n{gate_name.upper()} Gate:")
    for input_vec in INPUTS:
        output = calculate_output(weights, input_vec, bias)
        print(f"Input: {input_vec}, Output: {output}")

# AND and OR gate outputs
and_outputs = np.array([1, -1, -1, -1])
or_outputs = np.array([1, 1, 1, -1])

# Print results for both gates
train_and_print("AND", and_outputs)
train_and_print("OR", or_outputs)""")
def third():
    print("""import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Generate a larger synthetic dataset (100 crabs with features: shell width, claw size, weight)
np.random.seed(100)
blue_crabs = np.random.normal([5.5, 3.0, 0.4], 0.5, (50, 3))  # 50 Blue crabs
orange_crabs = np.random.normal([6.0, 3.5, 0.5], 0.5, (50, 3)) # 50 Orange crabs

# Combine the data and create labels (0 = Blue, 1 = Orange)
data = np.vstack((blue_crabs, orange_crabs))
labels = np.array([0] * 50 + [1] * 50)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Build and compile the neural network (PatternNet)
model = Sequential([
    Dense(5, input_dim=3, activation='relu'),  # 3 input features (shell width, claw size, weight)
    Dense(5, activation='relu'),
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=4, verbose=0)  # Train the model

# Evaluate the model on the test data
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Predict species for a new crab (e.g., shell width, claw size, weight)
new_crab = np.array([[5.9, 3.3, 0.55]])
prediction = (model.predict(new_crab) > 0.5).astype(int)
species = ["Blue", "Orange"]
print(f"The predicted species for the new crab is: {species[prediction[0][0]]}")""")
    
def four():
   print("""import torch
import torch.nn as nn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Data
X, y = load_wine(return_X_y=True)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = nn.Sequential(
    nn.Linear(X_train.shape[1], 10),
    nn.ReLU(),
    nn.Linear(10, 3)
)

# Training
X_train, y_train = torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for _ in range(1000):
    optimizer.zero_grad()
    loss = loss_fn(model(X_train), y_train)
    loss.backward()
    optimizer.step()

# Evaluation
X_test = torch.tensor(X_test, dtype=torch.float32)
_, predicted = torch.max(model(X_test), 1)
accuracy = (predicted == torch.tensor(y_test)).float().mean().item()

print(f'Accuracy: {accuracy * 100:.2f}%')""")

# Naive Bayes function
def five():
    print("""import torch

# Define operations as lambda functions
add = lambda a, b: a + b
sub = lambda a, b: a - b
mul = lambda a, b: a * b
div = lambda a, b: a / b if (b != 0).all() else "Error! Division by zero."

# Example usage
x, y = torch.tensor([10.0]), torch.tensor([5.0])

print(f"Add: {add(x, y).item()}")
print(f"Sub: {sub(x, y).item()}")
print(f"Mul: {mul(x, y).item()}")
print(f"Div: {div(x, y)}")""")
    
def six():
    print("""import numpy as np

# Data and labels
X = np.array([[2, 3], [1, 1], [2, 1], [3, 3], [2, 2]])
y = np.array([1, -1, -1, 1, -1])

# LMS algorithm
w, b, lr = np.zeros(2), 0, 0.01
for _ in range(1000):
    for i in range(len(X)):
        y_pred = np.dot(X[i], w) + b
        error = y[i] - y_pred
        w += lr * error * X[i]
        b += lr * error

# Prediction
pred = np.sign(np.dot(X, w) + b)
print(f"Final Weights: {w}, Bias: {b}, Predictions: {pred}")""")
    
def seven():
    print("""import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Generate synthetic time series data (replace with real dataset)
np.random.seed(42)
data = np.sin(np.arange(0, 100, 0.1)) + np.random.normal(0, 0.1, 1000)  # Sine wave with noise
data = data.reshape(-1, 1)

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Function to create sequences from data
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

# Hyperparameters
seq_length = 50  # Length of the input sequence
train_size = int(len(scaled_data) * 0.8)

# Create training and test datasets
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

x_train, y_train = create_sequences(train_data, seq_length)
x_test, y_test = create_sequences(test_data, seq_length)

# Build LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(seq_length, 1)))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_test, y_test))

# Make predictions
predicted = model.predict(x_test)
predicted = scaler.inverse_transform(predicted)  # Inverse scaling

# Plot results
actual = scaler.inverse_transform(y_test.reshape(-1, 1))
plt.plot(actual, label='Actual Data')
plt.plot(predicted, label='Predicted Data')
plt.legend()
plt.show()""")
    
def eight():
    print("""import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load a sample dataset (IMDB movie reviews for binary sentiment analysis)
max_words = 10000
max_len = 500
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

# Pad sequences to ensure consistent input length
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# One-hot encode the labels
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Define an RNN model
model = Sequential([
    SimpleRNN(64, input_shape=(max_len, 1), return_sequences=False),
    Dense(2, activation='softmax')
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=1, batch_size=64,
                    validation_data=(x_test, y_test), verbose=1)

# Plot accuracy and loss
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy}")
print(f"Test Loss: {test_loss}")

# Generate predictions and classification report
y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_true, y_pred_classes))

# Confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred_classes)
print("\nConfusion Matrix:")
print(conf_matrix)""")
    
def nine():
    print("""import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.applications import InceptionV3, ResNet50, VGG16
from tensorflow.keras.applications.inception_v3 import preprocess_input as inception_preprocess
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix

# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Preprocess data by resizing to fit each model's expected input shape
img_size = 224  # Resizing to 224x224 as expected by most ImageNet models
x_train = tf.image.resize(x_train, (img_size, img_size))
x_test = tf.image.resize(x_test, (img_size, img_size))

# Convert labels to categorical (10 classes in CIFAR-10)
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Define a function to evaluate a model and calculate inference time
def evaluate_model(model, x_test, y_test, preprocess_func):
    # Preprocess test images
    x_test_processed = preprocess_func(x_test)

    # Evaluate model on test data
    start_time = time.time()
    test_loss, test_accuracy = model.evaluate(x_test_processed, y_test, verbose=0)
    end_time = time.time()

    # Calculate inference time
    inference_time = end_time - start_time

    # Generate predictions and classification report
    y_pred = model.predict(x_test_processed)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = np.argmax(y_test, axis=1)
    report = classification_report(y_true, y_pred_classes)
    confusion = confusion_matrix(y_true, y_pred_classes)

    return test_accuracy, test_loss, inference_time, report, confusion

# Load pre-trained models with ImageNet weights
models = {
    'InceptionV3': (InceptionV3(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3)), inception_preprocess),
    'ResNet50': (ResNet50(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3)), resnet_preprocess),
    'VGG16': (VGG16(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3)), vgg_preprocess),
}

# Evaluate each model and print results
for model_name, (model, preprocess_func) in models.items():
    print(f"\nEvaluating model: {model_name}")
    model.trainable = False  # Freeze layers for evaluation

    # Add a global average pooling and dense layer for CIFAR-10 classification
    model_with_top = tf.keras.models.Sequential([
        model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # Compile the model
    model_with_top.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Evaluate the model
    test_accuracy, test_loss, inference_time, report, confusion = evaluate_model(model_with_top, x_test, y_test, preprocess_func)

    # Print results
    print(f"Test Accuracy: {test_accuracy}")
    print(f"Test Loss: {test_loss}")
    print(f"Inference Time: {inference_time} seconds")
    print("\nClassification Report:\n", report)
    print("Confusion Matrix:\n", confusion)""")
def Ten():
    print("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from tensorflow.keras.optimizers import Adam

# Load historical stock data
ticker = 'AAPL'  # You can replace this with any other stock ticker
start_date = '2015-01-01'
end_date = '2023-01-01'
data = yf.download(ticker, start=start_date, end=end_date)

# Preprocess the data
# We will use the 'Close' prices for this example
data = data[['Close']].dropna()
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create sequences for time series forecasting
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

sequence_length = 60  # Number of days to use for each prediction
X, y = create_sequences(scaled_data, sequence_length)

# Split data into training and testing sets
split_ratio = 0.8
split = int(split_ratio * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Define the GRU model
model = Sequential([
    GRU(64, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    GRU(32, return_sequences=False),
    Dense(1)
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Predict on the test set
y_pred = model.predict(X_test)

# Rescale the predictions and actual values back to the original scale
y_pred_rescaled = scaler.inverse_transform(y_pred)
y_test_rescaled = scaler.inverse_transform(y_test)

# Plot the results
plt.figure(figsize=(14, 5))
plt.plot(data.index[-len(y_test):], y_test_rescaled, color='blue', label='Actual Stock Price')
plt.plot(data.index[-len(y_test):], y_pred_rescaled, color='red', label='Predicted Stock Price')
plt.title(f'{ticker} Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

# Evaluate model performance
mse = np.mean(np.square(y_test_rescaled - y_pred_rescaled))
rmse = np.sqrt(mse)
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")""")