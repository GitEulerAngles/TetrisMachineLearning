from pyboy import pyboy
from machine import machine
from gameboy import game
from time import time
import tensorflow as tf
print(tf.__version__)

amount_of_games = 1
games = []
models = []
game_over = []

for i in range(amount_of_games):
    game_over.append(0)
    newModel = machine()
    if amount_of_games == 0:
        newModel.model = newModel.model.load_weights("C:/PythonSaves/Emulator/model.h5")
    models.append(newModel)
    newGame = game()
    newGame.emulation.tick()
    for i in range(170):
        newGame.emulation.send_input(pyboy.WindowEvent.PRESS_BUTTON_START)
        newGame.emulation.tick()
        newGame.emulation.send_input(pyboy.WindowEvent.RELEASE_BUTTON_START)
        newGame.emulation.tick()
    games.append(newGame)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

reset = 0
clock = 0
while 1:
    clock += 1
    for i in range(amount_of_games):
        if games[i].wrap.game_over():
            if game_over[i] == 0:
                game_over[i] = 1
                reset += 1
        games[i].updateData()
        button = -1
        if clock >= 80:
            button = models[i].runModel(games[i].game_tiles)
            if i == amount_of_games-1:
                clock = 0
        if (game_over[i] == 0):
            games[i].runGame(button)
    if (reset == amount_of_games):
        maxIndex = 0
        reset = 0
        for i in range(amount_of_games):
            game_over[i] = 0
            lineCoverage = 0

            for y in range(0,18):
                count = 0
                for x in range(0,10):
                    if (games[i].game_tiles[y][x] == 1):
                        count += 1
                lineCoverage += count^2

            for x in range(0,10):
                penalty = False
                for y in range(17,-1,-1):
                    if (games[i].game_tiles[y][x] == 1):
                        penalty = True
                    if (games[i].game_tiles[y][x] == 0 and penalty):
                        games[i].fitNess -= 5

            games[i].fitNess += games[i].wrap.score*20
            games[i].fitNess += lineCoverage

            if games[i].fitNess > games[maxIndex].fitNess:
                maxIndex = i
        
        print("Max index for that generation: " + str(games[maxIndex].fitNess))

        models[maxIndex].model.save_weights("model.h5")
        for i in range(amount_of_games):
            games[i].fitNess = 0

            if i == maxIndex:
                continue
            models[i].model.set_weights(models[maxIndex].model.get_weights())
            models[i].randomFit(.1,10.0)
        for i in range(amount_of_games):
            while (games[i].tile[0,0] == 298):
                games[i].emulation.send_input(pyboy.WindowEvent.PRESS_BUTTON_START)
                games[i].emulation.tick()
                games[i].emulation.send_input(pyboy.WindowEvent.RELEASE_BUTTON_START)
                games[i].emulation.tick()
