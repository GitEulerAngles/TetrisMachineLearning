from draw import *

background_colour = (30, 30, 30) 

def load_games(screen, running, neuralnets, games):
    reset = False
    while not reset and running:
        reset = True
        for g in range(len(games)):
            reset = reset and games[g].game_over

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

        for i, game in enumerate(games):
            if not game.game_over:
                update_game(game, neuralnets[i])

        highest_net = 0
        for neuralnet in range(len(neuralnets)):
            if (neuralnets[neuralnet].fitness > neuralnets[highest_net].fitness):
                highest_net = neuralnet

        screen.fill(background_colour)

        for i, game in enumerate(games):
            draw_game(screen, game, i, i == highest_net)
            draw_piece(screen, game, i)

        pygame.display.flip()

    return running
