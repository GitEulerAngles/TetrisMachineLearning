import pygame
from machine import *
from game import *
from tetris import Game

neuralnets = [NeuralNet() for _ in range(1)]
games = [Game() for _ in range(1)]

def main_loop():
    #saved_nn = None
    running = True

    if os.path.exists('fit_model.keras'):
        for neuralnet in neuralnets:
            neuralnet.model = tf.keras.models.load_model('fit_model.keras')
    else:
        print('Couldn\'t load tensorflow model') 

    while running:
        for neuralnet in neuralnets:
            neuralnet.right = [0,0]
        
        for game in games:
            game.setup()
            game.best_move = find_move(deepcopy(game), [22.6, 7.6, 14.2, 0.3,  7.6, 8.5])

        running = load_games(screen, running, neuralnets, games)

        highest_score = (-float('inf'), -1)

        for i, network in enumerate(neuralnets):
            if (highest_score[0] < network.right[0]):
                highest_score = (network.right[0], i)

        #saved_nn = tf.keras.models.clone_model(neuralnets[highest_score[1]].model)
        neuralnets[highest_score[1]].model.save('fit_model.keras')

        with open('data', 'a') as file:
            frac = 0
            if (neuralnets[highest_score[1]].right[1] != 0):
                frac = neuralnets[highest_score[1]].right[0] / neuralnets[highest_score[1]].right[1] * 100
            file.write(str(frac) + '\n')

        #for network in neuralnets:
        #    if (saved_nn is not None and highest_score != network.right[0]):
        #        network.set_weights(deepcopy(saved_nn.get_weights()))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 1000))
    pygame.display.set_caption('Tetris')

    main_loop()

    pygame.quit()
