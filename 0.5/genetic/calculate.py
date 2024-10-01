from copy import deepcopy

def calculate_game(game, params):
    holes_cost, bump, pit_cost, ragged, low, tetris = params
    score = 100

    #penalize holes
    for x in range(10):
        holes = False
        for y in range(20):
            tile_type = game.tiles[x][y]
            if tile_type == 1:
                holes = True
            elif holes == True:
                score -= holes_cost

    #penalize bumpiness
    #highest = [20] * 10 
    #for x in range(10):
    #    for y in range(19, -1, -1):
    #        if game.tiles[x][y] == 1:
    #            highest[x] = y
    #            break

    #bumpiness = 0
    #for x in range(9):
    #    bumpiness += abs(highest[x] - highest[x + 1])

    #score -= bumpiness*bump

    #penalize three deep
    #holes = 0
    #for x in range(10):
    #    hole_count = 0
    #    for y in range(20):
    #        if (game.tiles[x][y] == 1):
    #            break
    #        if ((x == 0 or game.tiles[x-1][y] == 1) and (x == 9 or game.tiles[x+1][y] == 1)):
    #            hole_count += 1
    #        if hole_count > 2:
    #            holes += 1

    #score -= holes * pit_cost

    #keep ragged
    #for x in range(8,0,-1):
    #    for y in range(19):
    #        if game.tiles[x][y] == 1 and game.tiles[x][y - 1] == 0:
    #            if game.tiles[x+1][y] == 0 and game.tiles[x+1][y+1] == 1:
    #                score += ragged
    #            if game.tiles[x-1][y] == 0 and game.tiles[x-1][y+1] == 1:
    #                score += ragged

    #reward being low
    score += game.piece_pos[1] * game.piece_pos[1] / low

    #reward tetris
    score += check_for_tetris(deepcopy(game)) * tetris

    return score

def bring_down(game, y):
    for current_y in range(y, 0, -1):
        for x in range(10):
            game.tiles[x][current_y] = game.tiles[x][current_y-1]
    for x in range(10):
        game.tiles[x][0] = 0

def check_for_tetris(game):
    tetris = 0
    y = 19
    while y >= 0:
        row_filled = True
        for x in range(10):
            if game.tiles[x][y] != 1:
                row_filled = False
                break
        if row_filled:
            tetris += 1
            bring_down(game, y)
        else:
            y -= 1
    
    game.score += tetris

    return tetris
