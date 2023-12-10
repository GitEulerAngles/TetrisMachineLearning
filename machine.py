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
        self.randomFit(.2,10)
    
    def randomFit(self, scale=.2, max=10.0):
        for layer in self.model.layers:
            if hasattr(layer, 'weights'):
                weights = layer.get_weights()
                for i, w in enumerate(weights):
                    r = (np.random.random(w.shape) * scale * 2) - scale
                    weights[i] = tf.where(tf.less(w + r, -max), -max, tf.where(tf.greater(w + r, max), max, w + r))
                layer.set_weights(weights)
            if hasattr(layer, 'biases'):
                biases = layer.get_weights()
                for i, b in enumerate(biases):
                    r = (np.random.random(b.shape) * scale * 2) - scale
                    biases[i] = tf.where(tf.less(b + r, -max), -max, tf.where(tf.greater(b + r, max), max, b + r))
                layer.set_weights(biases)

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

    checkPoint = 0
    bestScore = 0
    def evalModel(self, fitNess):
        global checkPoint, bestScore

        if (fitNess > bestScore):
            print("Saving...")
            bestScore = fitNess
            self.model.save_weights("model.h5")
        else:
            checkPoint += 1

        fitNess = 0

        if checkPoint > 3:
            print("Loading...")
            checkPoint = 0
            self.model.load_weights("C:/PythonSaves/Emulator/model.h5")

        self.randomFit(self.model)

        #for i in range(50):
        #    print(bestScore)
        #    emulation.send_input(pyboy.WindowEvent.RELEASE_BUTTON_A)
        #    emulation.tick()
        #    emulation.send_input(pyboy.WindowEvent.PRESS_BUTTON_A)
        #    emulation.tick()
