import pyxel


class Player:
    IMG = 0
    WIDTH = 8
    HEIGHT = 8
    SPEED = 1

    ACTIONS = {
        "static": (0, 0),
        "punch": (8, 0),
        "kick": (0, 8),
        "headbutt": (8, 8),
    }

    def __init__(self):
        self.action = "static"
        self.x = pyxel.width / 3
        self.y = pyxel.height - Player.HEIGHT

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.x -= Player.SPEED
        elif pyxel.btn(pyxel.KEY_D):
            self.x += Player.SPEED

    def draw(self):
        current_action_coordinates = Player.ACTIONS[self.action]
        pyxel.blt(
            self.x,
            self.y,
            Player.IMG,
            current_action_coordinates[0],
            current_action_coordinates[1],
            Player.WIDTH,
            Player.HEIGHT,
        )


class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("fightbattle.pyxres")
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()


App()
