from draw import pieces
from random import randrange

class Game:
    def __init__(self):
        self.tiles = []
        self.piece = []
        self.piece_type = 1
        self.piece_pos = [4, 0]
        self.best_move = ()
        self.rot = 1
        self.score = 0
        self.game_over = False
        self.piece_bag = [0,1,2,3,4,5,6]
        self.setup()

    def setup(self):
        self.tiles = []
        self.score = 0
        self.game_over = False
        for x in range(10):
            row = []
            for y in range(20):
                row.append(0)
            self.tiles.append(row)

        self.random()

    def random(self):
        r = randrange(0, len(self.piece_bag))

        self.piece_type = self.piece_bag[r]
        self.piece_bag.pop(r)

        self.piece = pieces[self.piece_type]

        if (len(self.piece_bag) == 0):
            self.piece_bag = [0,1,2,3,4,5,6]

