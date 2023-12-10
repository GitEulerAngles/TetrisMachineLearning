import tensorflow as tf
import numpy as np

class machine:
    model = 0
    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='linear', input_shape=(180,)),
            tf.keras.layers.Dense(20, activation='linear'),
            tf.keras.layers.Dense(10, activation='linear'),
            tf.keras.layers.Dense(5, activation='linear')
        ])

        self.model.compile(optimizer='adam', loss='binary_crossentropy')
    
    def randomFit(self, scale=.2, max_value=10.0):
        for layer in self.model.layers:
            current_weights = layer.get_weights()
            new_weights = []
            for w in current_weights:  # This will loop over weights and biases together
                r = (np.random.random(w.shape) * scale * 2) - scale
                # Apply the randomness
                modified_w = np.clip(w + r, -max_value, max_value)
                new_weights.append(modified_w)
            layer.set_weights(new_weights)

    def runModel(self, game_tiles):
        inputData = []
        for y in range(0,18):
            for x in range(0,10):
                inputData.append(game_tiles[y][x])

        inputData = tf.convert_to_tensor(inputData, dtype=tf.float32)
        inputData = tf.reshape(inputData, (1, 180))
        
        predictions = self.model.predict(inputData)[0]

        maxIndex = 0
        for i in range(1,5):
            if predictions[i] > predictions[maxIndex]:
                maxIndex = i
        
        return maxIndex
