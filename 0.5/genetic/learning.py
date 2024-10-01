import pygame
from machine import *
from game import *
from tetris import Game

neuralnets = [NeuralNet() for _ in range(18)]
games = [Game() for _ in range(18)]

def main_loop():
    saved_nn = None
    running = True

    try:
        for neuralnet in neuralnets:
            neuralnet.model = tf.keras.models.load_model('fit_model.h5')
    except IOError:
        print('Couldn\'t load tensorflow model')

    while running:
        for neuralnet in neuralnets:
            neuralnet.fitness = 0
        
        for game in games:
            game.setup()

        running = load_games(screen, running, neuralnets, games)

        highest_score = (-float('inf'), -1)

        for i, network in enumerate(neuralnets):
            if (highest_score[0] < network.fitness):
                highest_score = (network.fitness, i)

        saved_nn = tf.keras.models.clone_model(neuralnets[highest_score[1]].model)
        neuralnets[highest_score[1]].model.save('fit_model.h5')

        with open('data', 'a') as file:
            file.write(str(highest_score[0]) + '\n')

        for network in neuralnets:
            if (saved_nn is not None and highest_score != network.fitness):
                network.set_weights(deepcopy(saved_nn.get_weights()))
                network.set_weights(mutation(network.get_weights()))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Tetris')

    main_loop()

    pygame.quit()
