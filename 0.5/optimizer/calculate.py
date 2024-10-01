from draw import check_collision, rotate_piece, check_for_tetris
from copy import deepcopy

def find_move(game, params):
    moves = []

    for rotation in range (4):
        game.rot = rotation
        game.piece_pos = [1,0]
        rotate_piece(game)
        find_left_pos(game)

        not_right = True
        while not_right:
            find_bottom_pos(game)
            calculate_game(deepcopy(game), moves, params)

            if (check_right(game)):
                not_right = False

            game.piece_pos[1] = 0
            game.piece_pos[0] += 1

    return max(moves, key=lambda x: x[0])

def calculate_game(game, moves, params):
    holes_cost, bump, pit_cost, ragged, low, tetris = params
    score = 0

    place_piece(game)

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
    highest = [20] * 10 
    for x in range(10):
        for y in range(19, -1, -1):
            if game.tiles[x][y] == 1:
                highest[x] = y
                break

    bumpiness = 0
    for x in range(9):
        bumpiness += abs(highest[x] - highest[x + 1])

    score -= bumpiness*bump

    #penalize three deep
    holes = 0
    for x in range(10):
        hole_count = 0
        for y in range(20):
            if (game.tiles[x][y] == 1):
                break
            if ((x == 0 or game.tiles[x-1][y] == 1) and (x == 9 or game.tiles[x+1][y] == 1)):
                hole_count += 1
            if hole_count > 2:
                holes += 1

    score -= holes * pit_cost

    #keep ragged
    for x in range(8,0,-1):
        for y in range(19):
            if game.tiles[x][y] == 1 and game.tiles[x][y - 1] == 0:
                if game.tiles[x+1][y] == 0 and game.tiles[x+1][y+1] == 1:
                    score += ragged
                if game.tiles[x-1][y] == 0 and game.tiles[x-1][y+1] == 1:
                    score += ragged

    #reward being low
    if low != 0:
        score += game.piece_pos[1] * game.piece_pos[1] / low

    #reward tetris
    score += check_for_tetris(deepcopy(game)) * tetris

    moves.append((score, game.piece_pos, game.rot))

def place_piece(copy_game):
    for y in range(4):
        for x in range(4):
            tile_type = copy_game.piece[x][y]
            if (tile_type == 1):
                game_pos = (copy_game.piece_pos[0]+x, copy_game.piece_pos[1]+y)
                copy_game.tiles[game_pos[0]][game_pos[1]] = copy_game.piece[x][y]

def find_left_pos(game):
    not_bounded = True
    while not_bounded:
        game.piece_pos[0] -= 1

        for y in range(4):
            for x in range(4):
                game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

                tile_type = game.piece[x][y]

                if (tile_type == 1 and game_pos[0] <= 0):
                    not_bounded = False

def find_bottom_pos(game):
    not_bounded = True
    while not_bounded:
        game.piece_pos[1] += 1

        if (check_collision(game)):
            game.piece_pos[1] -= 1
            not_bounded = False
        else:
            for y in range(4):
                for x in range(4):
                    game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

                    tile_type = game.piece[x][y]

                    if (tile_type == 1 and game_pos[1] >= 19):
                        not_bounded = False

def check_right(game):
    for y in range(4):
        for x in range(4):
            game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

            tile_type = game.piece[x][y]

            if (tile_type == 1 and game_pos[0] >= 9):
                return True
            
    return False
