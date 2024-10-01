from pyboy import PyBoy, pyboy

class game:
    fitNess = 0
    emulation = 0
    wrap = 0
    tile = 0
    newBlock = True
    game_tiles = []
    scores = 0
    def __init__(self):
        self.emulation = PyBoy('C:/PythonSaves/Tetris.gb', window_type="SDL2", window_scale=3, debug = False, game_wrapper=True)
        self.wrap = self.emulation.game_wrapper()
        self.tile = self.emulation.botsupport_manager().tilemap_window()
        self.emulation.set_emulation_speed(0)
        self.emulation.botsupport_manager().tilemap_background()

        for y in range(0, 18):
            row = []
            for x in range(0, 10):
                row.append(0)
            self.game_tiles.append(row)

    def updateData(self):
        #Tiles
        for y in range(0,18):
            for x in range(2,12):
                if (self.tile[x,y] == 303):
                    self.game_tiles[y][x-2] = 0
                elif (self.tile[x,y] != 135):
                    self.game_tiles[y][x-2] = 1

        #Sprites
        for i in range(4,8):
            x = int((self.emulation.botsupport_manager().sprite(i).x/8)-2)
            y = int(self.emulation.botsupport_manager().sprite(i).y/8)

            if (y == 2 and self.newBlock):
                self.fitNess += 1
                self.newBlock = False

            if (y == 10):
                self.newBlock = True

            if x >= 0 and y >= 0 and x < 10 and y < 18:
                self.game_tiles[y][x] = 2
            
    def runGame(self, move):
        if self.tile[0,0] == 298 and move != -1:
            x = 0

            if move == 0:
                x = pyboy.WindowEvent.PRESS_ARROW_LEFT
            elif move == 1:
                x = pyboy.WindowEvent.PRESS_ARROW_RIGHT
            elif move == 2:
                x = pyboy.WindowEvent.PRESS_ARROW_DOWN
            elif move == 3:
                x = pyboy.WindowEvent.PRESS_BUTTON_B
            elif move == 4:
                x = pyboy.WindowEvent.PRESS_BUTTON_A
            self.emulation.send_input(x)
            self.emulation.tick()
            self.emulation.send_input(x+8)
            self.emulation.tick()
        else:
            self.emulation.tick()
