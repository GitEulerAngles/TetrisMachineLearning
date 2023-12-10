from pyboy import pyboy
from machine import machine
from gameboy import game
from time import time

amount_of_games = 1
games = []
models = []
game_over = []

for i in range(amount_of_games):
    game_over.append(0)
    newModel = machine()
    if i == 0:
        newModel.model.load_weights("C:/PythonSaves/Emulator/model.h5")
    else:
        newModel.randomFit(.2, 10)
    models.append(newModel)
    newGame = game()
    newGame.emulation.tick()
    for i in range(170):
        newGame.emulation.send_input(pyboy.WindowEvent.PRESS_BUTTON_START)
        newGame.emulation.tick()
        newGame.emulation.send_input(pyboy.WindowEvent.RELEASE_BUTTON_START)
        newGame.emulation.tick()
    games.append(newGame)

reset = 0
clock = 0
while 1:
    clock += 1
    for i in range(amount_of_games):
        if games[i].wrap.game_over():
            if game_over[i] == 0:
                game_over[i] = 1
                reset += 1
        if (game_over[i] == 0):
            games[i].updateData()
            button = -1
            if clock >= 100:
                button = models[i].runModel(games[i].game_tiles)
                if i == amount_of_games-1:
                    clock = 0
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

            games[i].fitNess += games[i].wrap.score
            games[i].fitNess += lineCoverage

            if games[i].fitNess > games[maxIndex].fitNess:
                maxIndex = i
        
        print("Max index for that generation: " + str(games[maxIndex].fitNess))

        models[maxIndex].model.save_weights("C:/PythonSaves/Emulator/model.h5")
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
