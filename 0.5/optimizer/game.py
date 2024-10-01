import pygame 
from tetris import Game
from calculate import *
from draw import *
from scipy.optimize import differential_evolution


background_colour = (30, 30, 30) 
screen = pygame.display.set_mode((1920, 1080)) 
pygame.display.set_caption('Tetris') 

running = True

games = [Game() for _ in range(1)]
highest_score = 0

def load_game(params):
    for i in range(len(games)):
        games[i].setup()

    print(params)

    global running, highest_score
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

        screen.fill(background_colour)

        reset = True
        for g in range(len(games)):
            reset = reset and games[g].game_over

        for i in range(len(games)):
            if (reset):
                score = sum(game.score for game in games) / len(games)
                if (score > highest_score):
                    highest_score = score
                    with open("optimal_params.txt", "w") as file:
                        file.write(f"Optimal parameters: {params}\n")
                        file.write(f"Maximum x: {score}\n")
                return -score
            elif not games[i].game_over:
                if (games[i].piece_pos[1] == 0):
                    games[i].best_move = find_move(deepcopy(games[i]), params)
                update_game(games[i])
            
            draw_game(screen, games[i], i)
            draw_piece(screen, games[i], i)

        pygame.display.flip()

def run_optimization():
    bounds = [(0, 60), (0, 15), (0, 15), (0, 15), (0, 15), (0, 15)]

    result = differential_evolution(
            load_game, 
            bounds, 
            maxiter=100,
            popsize=15,
            tol=0.5
        )
    optimal_params = result.x
    optimal_x = -result.fun

    print(f"Optimal parameters (a, b, c): {optimal_params}")
    print(f"Maximum x: {optimal_x}")

    with open("optimal_params.txt", "w") as file:
        file.write(f"Optimal parameters: {optimal_params}\n")
        file.write(f"Maximum x: {optimal_x}\n")

load_game([22.64492475, 7.61958583, 14.17247122, 0.25931778,  7.62838852, 8.53580599])

#run_optimization()
