import pygame
import numpy as np
from calculate import *
from copy import deepcopy
from math import floor

color = [(45,45,45), (255,255,255)]

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

size = 20

def draw_piece(screen, game, pos):
    game_pos = (floor(pos*size*10 % 1800), floor(pos*size*10 / 1800)*size*size)

    for y in range(4):
        for x in range(4):
            tile_type = game.piece[x][y]

            if tile_type == 0:
                continue

            pos_x = (x + game.piece_pos[0])*size + game_pos[0]
            pos_y = (y + game.piece_pos[1])*size + game_pos[1]

            pygame.draw.rect(screen, color[tile_type], (pos_x,pos_y,size,size))

def draw_game(screen, game, pos, highest):
    game_pos = (floor(pos*size*10 % 1800), floor(pos*size*10 / 1800)*size*size)

    for y in range(20):
        for x in range(10):
            tile_type = game.tiles[x][y]
            if (tile_type == 0 and highest):
                pygame.draw.rect(screen, (90,45,45), (x*size + game_pos[0],y*size + game_pos[1],size,size))
            else:
                pygame.draw.rect(screen, color[tile_type], (x*size + game_pos[0],y*size + game_pos[1],size,size))

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

def lay_down(game, neuralnet):
    for y in range(4):
        for x in range(4):
            tile_type = game.piece[x][y]
            if (tile_type == 1):
                game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

                if game_pos[0] < 0 or game_pos[0] >= len(game.tiles) or game_pos[1] < 0 or game_pos[1] >= len(game.tiles[0]):
                    continue

                game.tiles[game_pos[0]][game_pos[1]] = game.piece[x][y]

    neuralnet.fitness += calculate_game(deepcopy(game), [22.6, 7.6, 14.2, 0.3,  7.6, 8.5])

    check_for_tetris(game)

    game.random()
    game.piece_pos = [4,0]

    if (check_collision(game)):
        game.game_over = True

def rotate_piece(game):
    game.piece = deepcopy(pieces[game.piece_type])

    rotate = 3 if game.rot == 0 else 2

    for i in range(game.rot):
        rotatedPiece = [[0 for _ in range(4)] for _ in range(4)]
        for x in range(4):
            for y in range(4):
                rotatedPiece[y][rotate - x] = game.piece[x][y]

        game.piece = rotatedPiece

def update_game(game, neuralnet):
    neuralnet.clock += 1
    move = -1
    if (neuralnet.clock > 2):
        input_tiles = deepcopy(game.tiles)
        for y in range(4):
            for x in range(4):
                tile_type = game.piece[x][y]
                if (tile_type == 1):
                    game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

                    if game_pos[0] < 0 or game_pos[0] >= len(game.tiles) or game_pos[1] < 0 or game_pos[1] >= len(game.tiles[0]):
                        continue

                    input_tiles[game_pos[0]][game_pos[1]] = game.piece[x][y]+1
        
        move = neuralnet.predict(input_tiles)
        neuralnet.clock = 0

    if (move == 0):
        game.rot += 1
        rotate_piece(game)
        if (check_collision(game)):
            game.rot -= 1
    if (move == 1):
        game.piece_pos[0] += 1
        if (check_collision(game)):
            game.piece_pos[0] -= 1
    if (move == 2):
        game.piece_pos[0] -= 1
        if (check_collision(game)):
            game.piece_pos[0] += 1

    rotate_piece(game)

    game.piece_pos[1] += 1

    if (check_collision(game)):
        game.piece_pos[1] -= 1
        lay_down(game, neuralnet)
        return

    for y in range(4):
        for x in range(4):
            game_pos = (game.piece_pos[0]+x, game.piece_pos[1]+y)

            tile_type = game.piece[x][y]

            if (tile_type == 1 and game_pos[1] >= 19):
                lay_down(game, neuralnet)
