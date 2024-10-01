from draw import *

background_colour = (30, 30, 30) 

def load_games(screen, running, neuralnets, games):
    reset = False
    clock = 0
    while not reset and running:
        reset = True
        for g in range(len(games)):
            reset = reset and games[g].game_over

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

        for i, game in enumerate(games):
            if not game.game_over:
                update_game(game, neuralnets[i], get_move(neuralnets[i], game))

        highest_net = 0
        for neuralnet in range(len(neuralnets)):
            if (neuralnets[neuralnet].fitness > neuralnets[highest_net].fitness):
                highest_net = neuralnet

        clock += 1
        if (clock > 100):
            clock = 0
            frac = 0
            if (neuralnets[highest_net].right[1] != 0):
                frac = neuralnets[highest_net].right[0] / neuralnets[highest_net].right[1] * 100
            print(frac)

        screen.fill(background_colour)

        for i, game in enumerate(games):
            draw_game(screen, game, i, i == highest_net)
            draw_piece(screen, game, i)

        pygame.display.flip()

    return running
