import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
import sys, os

class NeuralNet:
    def __init__(self):
        self.fitness = 0
        self.clock = 0
        self.model = Sequential([
            Flatten(input_shape=(20, 10)),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(4, activation='softmax')
        ])
        self.model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        
    def predict(self, input_data):
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')

        predictions = self.model.predict(np.array(input_data).reshape(1, 20, 10))
        
        sys.stdout.close()
        sys.stdout = original_stdout
        
        return np.argmax(predictions)
    
    def get_weights(self):
        return self.model.get_weights()
    
    def set_weights(self, weights):
        self.model.set_weights(weights)

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
