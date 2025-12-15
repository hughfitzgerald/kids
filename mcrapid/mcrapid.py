import pyxel

SCREEN_HEIGHT = 120
SCREEN_WIDTH = 160

TILE_WIDTH = 8
TILE_HEIGHT = 8

ALL_BLACK = (0, 0)
DIRT = (0, 1)
GRASS = (1, 0)
STEVE = (1, 1)
LAVA = (2, 1)
WATER = (7, 1)
SOLID_BLOCKS = [DIRT, GRASS, LAVA]
NOT_SOLID_BLOCKS = [ALL_BLACK, WATER]


def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[0].pget(tile_x, tile_y)


class Camera:
    MARGIN = 0.3

    def __init__(self, x, y, target):
        self.target = target
        self.x = x
        self.y = y

    def update(self):
        margin_x = self.MARGIN * pyxel.width
        margin_y = self.MARGIN * pyxel.height
        self.x = max(
            min(self.x, self.target.x - margin_x),
            self.target.x + margin_x - pyxel.width,
            0,
        )
        self.y = max(
            min(self.y, self.target.y - margin_y),
            self.target.y + margin_y - pyxel.height,
            0,
        )


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
        self.punching = False
        self.punch_timer = 0

    def is_collide_by_coords(self, x, y, width, height):
        return (
            self.x < x + width
            and self.x + self.WIDTH > x
            and self.y < y + height
            and self.y + self.HEIGHT > y
        )

    def is_collide_by_tile(self, tile_x, tile_y):
        tile_px_x = tile_x * TILE_WIDTH
        tile_px_y = tile_y * TILE_HEIGHT
        return self.is_collide_by_coords(tile_px_x, tile_px_y, TILE_WIDTH, TILE_HEIGHT)

    def is_collide_solid_block(self):
        left_tile_x = int(self.x // TILE_WIDTH)
        right_tile_x = int((self.x + self.WIDTH) // TILE_WIDTH)
        top_tile_y = int(self.y // TILE_HEIGHT)
        bottom_tile_y = int((self.y + self.HEIGHT) // TILE_HEIGHT)

        for tile_x in range(left_tile_x, right_tile_x + 1):
            for tile_y in range(top_tile_y, bottom_tile_y + 1):
                if get_tile(tile_x, tile_y) not in NOT_SOLID_BLOCKS:
                    return True
        return False

    def move_with_collision_detect(self):
        self.y += self.y_velocity
        self.x += self.x_velocity
        if self.is_collide_solid_block():
            self.y -= self.y_velocity
            if self.is_collide_solid_block():
                self.y += self.y_velocity
                self.x -= self.x_velocity
                if self.is_collide_solid_block():
                    self.y -= self.y_velocity
                    self.y_velocity = 0
                    self.x_velocity = 0
                else:
                    self.x_velocity = 0
            else:
                self.y_velocity = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.y_velocity = self.JUMP_VELOCITY * -1

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.punching:
            self.punch_timer = 0
            self.punching = True

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

        self.move_with_collision_detect()

        self.y = max(self.y, 0)
        self.x = max(self.x, 0)

        if self.punching:
            self.punch_timer += 1
            if self.punch_timer > 8:
                self.punching = False

    def draw(self, camera):
        pyxel.blt(
            self.x - camera.x,
            self.y - camera.y,
            self.IMG,
            self.IMG_ORIGIN_X,
            self.IMG_ORIGIN_Y,
            self.WIDTH,
            self.HEIGHT,
        )
        if self.punching:
            punch_x = 6
            punch_y = 4
            punch_width = 3
            punch_height = 2
            punch_color = 15
            pyxel.rect(
                self.x - camera.x + punch_x,
                self.y - camera.y + punch_y,
                punch_width,
                punch_height,
                punch_color,
            )


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("mcrapid.pyxres")
        self.steve = Steve()
        self.camera = Camera(0, 0, self.steve)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.steve.update()
        self.camera.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, self.camera.x, self.camera.y, pyxel.width, pyxel.height)
        self.steve.draw(self.camera)


App()
