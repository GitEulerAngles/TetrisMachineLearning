import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras import losses

import numpy as np
import sys, os

class NeuralNet:
    def __init__(self):
        self.fitness = 0
        self.right = [0,0]
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            0.1,
            decay_steps=100000,
            decay_rate=0.96,
            staircase=True)

        optimizer = Adam(learning_rate=0.001)
        self.model = Sequential([
            Conv2D(16, (3, 3), activation='relu', input_shape=(10, 20, 1)),
            Flatten(),
            Dense(32, activation='relu'),
            Dense(4)  # Output Q-values for each action
        ])
        self.model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        
    def predict(self, input_data):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')

        predictions = self.model.predict(np.array(input_data).reshape(1, 10, 20, 1))
        
        sys.stdout.close()
        sys.stdout = original_stdout
        
        return np.argmax(predictions)
    
    def get_weights(self):
        return self.model.get_weights()
    
    def set_weights(self, weights):
        self.model.set_weights(weights)

def backpropagate(neuralnet, state, desired_move):
    state = np.array(state, dtype=np.float32).reshape(1, 10, 20, 1)
    desired_move = np.array([desired_move], dtype=np.int32)

    neuralnet.model.fit(state, desired_move, epochs=1, verbose=0)

def mutation(weights, mutation_rate=0.3, mutation_range=(-0.005, 0.005)):
    for array in weights:
        it = np.nditer(array, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            if np.random.rand() < mutation_rate:
                it[0] += np.random.uniform(mutation_range[0], mutation_range[1])
            it.iternext()
    return weights

def check_cuda():
    with open('cuda.txt', 'w') as file:
        file.write(f'Is built with CUDA: {tf.test.is_built_with_cuda()}\n')

        file.write("Available devices:\n")
        for device in tf.config.list_physical_devices():
            file.write(f'{device}\n')

        file.write(f"GPU devices:{tf.config.list_physical_devices('GPU')}\n")

check_cuda()
