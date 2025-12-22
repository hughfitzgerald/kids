import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

TILE_WIDTH = 8
TILE_HEIGHT = 8

ALL_BLACK = (0, 0)
SPECIAL_DANGER_BLOCK = (10, 1)
REPLACEMENT_DANGER_BLOCK = (31, 31)
NOT_SOLID_BLOCKS = [ALL_BLACK, (0, 4), (1, 4)]
DANGER_BLOCKS = [
    (1, 0),
    (3, 0),
    (4, 0),
    (4, 1),
    (6, 0),
    (7, 0),
    (10, 1),
    REPLACEMENT_DANGER_BLOCK,
]
NEXT_LEVEL_BLOCK = (2, 1)


def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[0].pget(tile_x, tile_y)


class Tilemap:
    STARTING_ROW = 4

    def __init__(self, id: int, x: int, y: int, w: int, h: int, colkey: int):
        self.id = id
        self.x = x
        self.y = y
        self.w, self.h = w, h
        self.colkey = colkey

        self.starting_tiles = {}

    def load_tilemap(self):
        tiles_x = self.w // 8
        tiles_y = self.h // 8

        for ty in range(tiles_y):
            for tx in range(tiles_x):
                tile_x = tx
                tile_y = ty
                tile_id = pyxel.tilemaps[self.id].pget(tile_x, tile_y)

                if tile_id[1] == self.STARTING_ROW:
                    self.starting_tiles[tile_id[0] + 1] = (
                        tile_x * 8 + self.x,
                        tile_y * 8 + self.y,
                    )
                    pyxel.tilemaps[self.id].pset(tile_x, tile_y, ALL_BLACK)
                elif tile_id == SPECIAL_DANGER_BLOCK:
                    pyxel.tilemaps[self.id].pset(
                        tile_x, tile_y, REPLACEMENT_DANGER_BLOCK
                    )


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


class Player:
    IMG = 0
    IMG_ORIGIN_X = 16
    IMG_ORIGIN_Y = 0
    WIDTH = 8
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
        self.is_dead = False
        self.next_level = False

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

    def colliding_tiles(self):
        colliding_tiles = []
        left_tile_x = int(self.x // TILE_WIDTH)
        right_tile_x = int((self.x + self.WIDTH) // TILE_WIDTH)
        top_tile_y = int(self.y // TILE_HEIGHT)
        bottom_tile_y = int((self.y + self.HEIGHT) // TILE_HEIGHT)

        for tile_x in range(left_tile_x, right_tile_x + 1):
            for tile_y in range(top_tile_y, bottom_tile_y + 1):
                colliding_tiles.append(get_tile(tile_x, tile_y))
        return colliding_tiles

    def is_collide_solid_block(self):
        colliding_tiles = self.colliding_tiles()

        for tile in colliding_tiles:
            if tile not in NOT_SOLID_BLOCKS:
                return True
        return False

    def is_collide_danger_block(self):
        colliding_tiles = self.colliding_tiles()

        for tile in colliding_tiles:
            if tile in DANGER_BLOCKS:
                return True
        return False

    def is_collide_next_level_block(self):
        colliding_tiles = self.colliding_tiles()

        for tile in colliding_tiles:
            if tile == NEXT_LEVEL_BLOCK:
                return True
        return False

    def move_with_collision_detect(self):
        self.y += self.y_velocity
        self.x += self.x_velocity

        if self.is_collide_next_level_block():
            self.next_level = True
            return

        if self.is_collide_danger_block():
            self.is_dead = True
            return

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


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("obstacle.pyxres")
        self.level = 1
        self.player = Player()
        self.camera = Camera(0, 0, self.player)
        self.tilemap = Tilemap(0, 0, 0, 256 * 8, 256 * 8, 0)
        self.tilemap.load_tilemap()
        self.player.x, self.player.y = self.tilemap.starting_tiles[self.level]
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.camera.update()

        if self.player.next_level:
            self.level += 1
            self.player.x, self.player.y = self.tilemap.starting_tiles[self.level]
            self.player.x_velocity = 0
            self.player.y_velocity = 0
            self.player.next_level = False

        if self.player.is_dead:
            self.player.x, self.player.y = self.tilemap.starting_tiles[self.level]
            self.player.x_velocity = 0
            self.player.y_velocity = 0
            self.player.is_dead = False

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, self.camera.x, self.camera.y, pyxel.width, pyxel.height)
        self.player.draw(self.camera)


App()
