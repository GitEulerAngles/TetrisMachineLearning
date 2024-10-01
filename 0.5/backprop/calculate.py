from copy import deepcopy
import numpy as np

pieces = np.array([
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ],[
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
])

rotation = np.array([
    [
        [[2, 0], [1, 1], [0, 2], [0, 0]],
        [[1, -1], [0, 0], [-1, 1], [0, 0]],
        [[0, -2], [-1, -1], [-2, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]]
    ],
    [
        [[0, 0], [-1, 1], [0, 0], [0, 0]],
        [[1, -1], [0, 0], [-1, 1], [-2, 2]],
        [[0, 0], [1, -1], [0, 0], [0, 0]],
        [[0, 0], [2, -2], [0, 0], [0, 0]]
    ]
])

def get_move(neuralnet, game):
    input_tiles = get_input_tiles(game)
    move = neuralnet.predict(input_tiles)

    return move

def get_input_tiles(game):
    input_tiles = deepcopy(game.tiles)

    for y in range(4):
        for x in range(4):
            tile_type = game.piece[x][y]
            if (tile_type == 1):
                game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

                if game_pos[0] < 0 or game_pos[0] >= len(game.tiles) or game_pos[1] < 0 or game_pos[1] >= len(game.tiles[0]):
                    continue

                input_tiles[game_pos[0]][game_pos[1]] = game.piece[x][y]+1

    noramlized_tiles = np.array(input_tiles) / 2.0

    return noramlized_tiles

def check_collision(game):
    for y in range(4):
        for x in range(4):
            game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

            tile_type = game.piece[x][y]

            if (tile_type == 1 and (game_pos[0] < 0 or game_pos[0] > 9 or game_pos[1] < 0 or game_pos[1] > 19)):
                return True

            if (tile_type == 1 and game.tiles[game_pos[0]][game_pos[1]] == 1):
                return True
    
    return False

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
            calculate_game(deepcopy(game), params, moves)

            if (check_right(game)):
                not_right = False

            game.piece_pos[1] = 0
            game.piece_pos[0] += 1

    return max(moves, key=lambda x: x[0])

def find_desired_move(game):
    if game.rot != game.best_move[2]:
        return 0
    elif game.piece_pos[0] > game.best_move[1][0]:
        return 2
    elif game.piece_pos[0] < game.best_move[1][0]:
        return 1
    else:
        return 3

def calculate_game(game, params, moves=None):
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
    score += game.piece_pos[1] * game.piece_pos[1] / low

    #reward tetris
    score += check_for_tetris(deepcopy(game)) * tetris

    if moves != None:
        moves.append((score, game.piece_pos, game.rot))
    else:
        return score

def rotate_piece(game):
    game.piece = deepcopy(pieces[game.piece_type])

    rotate = 3 if game.rot == 0 else 2

    for i in range(game.rot):
        rotatedPiece = [[0 for _ in range(4)] for _ in range(4)]
        for x in range(4):
            for y in range(4):
                rotatedPiece[y][rotate - x] = game.piece[x][y]

        game.piece = rotatedPiece

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

def place_piece(copy_game):
    for y in range(4):
        for x in range(4):
            tile_type = copy_game.piece[x][y]
            if tile_type == 1:
                game_pos_x = copy_game.piece_pos[0] + x
                game_pos_y = copy_game.piece_pos[1] + y
                if 0 <= game_pos_x < len(copy_game.tiles) and 0 <= game_pos_y < len(copy_game.tiles[0]):
                    copy_game.tiles[game_pos_x][game_pos_y] = tile_type

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

