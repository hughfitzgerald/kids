import pyxel

SCREEN_HEIGHT = 120
SCREEN_WIDTH = 160


class Steve:
    IMG = 0
    IMG_ORIGIN_X = 8
    IMG_ORIGIN_Y = 8
    WIDTH = 6
    HEIGHT = 8
    MAX_X_SPEED = 2
    MAX_Y_SPEED = 2
    GRAVITY = 0.2
    JUMP_VELOCITY = 4
    RUN_VELOCITY = 1
    FRICTION = 0.1

    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.y_velocity = self.JUMP_VELOCITY * -1

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x_velocity = self.RUN_VELOCITY * -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x_velocity = self.RUN_VELOCITY

        if self.x_velocity > 0:
            self.x_velocity -= self.FRICTION
            self.x_velocity = max(self.x_velocity, 0)
        if self.x_velocity < 0:
            self.x_velocity += self.FRICTION
            self.x_velocity = min(self.x_velocity, 0)

        self.y_velocity += self.GRAVITY
        self.y += self.y_velocity

        self.x += self.x_velocity

        self.y = max(min(self.y, pyxel.height - self.HEIGHT), 0)
        self.x = max(min(self.x, pyxel.width - self.WIDTH), 0)

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            self.IMG,
            self.IMG_ORIGIN_X,
            self.IMG_ORIGIN_Y,
            self.WIDTH,
            self.HEIGHT,
        )


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("mcrapid.pyxres")
        self.steve = Steve()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.steve.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        self.steve.draw()


App()
