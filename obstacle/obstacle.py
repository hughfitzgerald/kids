from collections import defaultdict
from itertools import product
import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

TILE_WIDTH = 8
TILE_HEIGHT = 8

ALL_BLACK = (0, 0)
NEXT_LEVEL_BLOCK = (2, 1)
SPECIAL_DANGER_BLOCK = (10, 1)
REPLACEMENT_DANGER_BLOCK = (31, 31)
REPLACEMENT_GEM_BLOCK = (31, 30)
FAKE_SMOKE = (21, 0)
REAL_SMOKE = (16, 0)
NOT_SOLID_BLOCKS = {
    ALL_BLACK,
    (11, 0),  # Water block
    REPLACEMENT_GEM_BLOCK,
    NEXT_LEVEL_BLOCK,
    FAKE_SMOKE,
}
DANGER_BLOCKS = {
    (4, 0),
    (4, 1),
    (10, 1),
    (17, 0),  # boss hair
    (17, 1),  # boss body
    REPLACEMENT_DANGER_BLOCK,
    REAL_SMOKE,
}
NOT_SOLID_BLOCKS.update(DANGER_BLOCKS)
DANGER_FROM_BELOW_BLOCKS = {(1, 0), (7, 0), (11, 1), (14, 0)}
DANGER_FROM_ABOVE_BLOCKS = {(3, 0), (6, 0), (14, 1)}

GREEN_GEM = (5, 0), (18, 0)
LIGHT_BLUE_GEM = (10, 0), (20, 0)
ORANGE_GEM = (9, 0), (16, 1)
DARK_BLUE_GEM = (15, 1), (18, 1)
RED_GEM = (12, 1), (19, 1)
MEDIUM_BLUE_GEM = (12, 0), (19, 0)
SPECIAL_GEM = (8, 0), (20, 1)

GEMS = {
    GREEN_GEM,
    LIGHT_BLUE_GEM,
    ORANGE_GEM,
    DARK_BLUE_GEM,
    RED_GEM,
    MEDIUM_BLUE_GEM,
    SPECIAL_GEM,
}
GEMS = {g[0]: g[1] for g in GEMS}

FRICTION = defaultdict(lambda: 0.2)
FRICTION[ALL_BLACK] = 0.05
FRICTION[(11, 0)] = 0.7  # water
FRICTION[(9, 1)] = 0.0  # ice


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
        self.gems = []

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
                elif tile_id in GEMS:
                    self.gems.append(
                        (
                            (
                                tile_x * 8 + self.x,
                                tile_y * 8 + self.y,
                            ),
                            tile_id,
                        )
                    )
                    pyxel.tilemaps[self.id].pset(tile_x, tile_y, REPLACEMENT_GEM_BLOCK)


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
    MAX_X_SPEED = 1.75
    MAX_Y_SPEED = 5
    GRAVITY = 0.3
    JUMP_VELOCITY = 4
    RUN_VELOCITY = 1

    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.is_dead = False
        self.next_level = False

    def kill(self):
        """Set player to dead"""
        self.is_dead = True
        pyxel.play(1, 1)  # play death sound

    def top_tiles(self, x, y):
        """Get the (up to two unique) tiles directly above the player at x,y"""
        tile_x1 = int(x // TILE_WIDTH)
        tile_x2 = tile_x1 + 1 if x % TILE_WIDTH else tile_x1
        tile_y = int(y // TILE_HEIGHT) - (1 if not y % TILE_HEIGHT else 0)
        return get_tile(tile_x1, tile_y), get_tile(tile_x2, tile_y)

    def bottom_tiles(self, x, y):
        """Get the (up to two unique) tiles directly beneath the player at x,y"""
        tile_x1 = int(x // TILE_WIDTH)
        tile_x2 = tile_x1 + 1 if x % TILE_WIDTH else tile_x1
        tile_y = int((y + self.HEIGHT) // TILE_HEIGHT)
        return get_tile(tile_x1, tile_y), get_tile(tile_x2, tile_y)

    def intersecting_tiles(self, x, y):
        """Return the (up to four unique) tiles intersecting the player at x, y

        Returns:
            tiles: Tile identities in order
                [(left, top), (left, bottom), (right, top), (right, bottom)]
        """
        tile_x1 = int(x // TILE_WIDTH)
        tile_x2 = int((x + self.WIDTH - 1) // TILE_WIDTH)
        tile_y1 = int(y // TILE_HEIGHT)
        tile_y2 = int((y + self.HEIGHT - 1) // TILE_HEIGHT)
        intersecting_tiles = []
        for tx, ty in product((tile_x1, tile_x2), (tile_y1, tile_y2)):
            intersecting_tiles.append(get_tile(tx, ty))
        return intersecting_tiles

    def any_solid_block(self, tiles):
        for tile in tiles:
            if tile not in NOT_SOLID_BLOCKS:
                return True
        return False

    def attempt_move(self, x, y, x_velocity, y_velocity):
        """Attempt move based on current position and velocity"""
        x_attempt = round(x + x_velocity)
        y_attempt = y + y_velocity
        intersecting_tiles = self.intersecting_tiles(x_attempt, y_attempt)

        # Search for collisions in our path
        xp = x
        yp = y
        # x_attempt_first = x_attempt # unused
        y_attempt_first = y_attempt
        scale = 1
        while abs(x_attempt - xp) > 0 or abs(y_attempt - yp) > 0:
            if self.any_solid_block(intersecting_tiles):
                # TODO binary search
                scale *= 0.9
                x_attempt = round(x + scale * x_velocity)
                y_attempt = y + scale * y_velocity
                intersecting_tiles = self.intersecting_tiles(x_attempt, y_attempt)
            else:
                # no longer blocked - return last successful position
                # if we got blocked in either dimension, set that velocity to zero
                # TODO: think carefully about x dimension
                if abs(y_attempt - y_attempt_first) >= 1:
                    y_velocity = 0
                return x_attempt, y_attempt, x_velocity, y_velocity

        return x_attempt, y_attempt, x_velocity, y_velocity

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.y_velocity = self.JUMP_VELOCITY * -1
            pyxel.play(2, 0)  # play jump sound

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x_velocity += self.RUN_VELOCITY * -1
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x_velocity += self.RUN_VELOCITY

        bt1, bt2 = self.bottom_tiles(self.x, self.y)
        friction = (FRICTION[bt1] + FRICTION[bt2]) / 2
        # print(friction)
        if self.x_velocity > 0:
            self.x_velocity -= friction
            self.x_velocity = max(self.x_velocity, 0)
        elif self.x_velocity < 0:
            self.x_velocity += friction
            self.x_velocity = min(self.x_velocity, 0)

        self.y_velocity += self.GRAVITY

        if self.x_velocity > self.MAX_X_SPEED:
            self.x_velocity = self.MAX_X_SPEED
        elif self.x_velocity < -self.MAX_X_SPEED:
            self.x_velocity = -self.MAX_X_SPEED
        if self.y_velocity > self.MAX_Y_SPEED:
            self.y_velocity = self.MAX_Y_SPEED
        elif self.y_velocity < -self.MAX_Y_SPEED:
            self.y_velocity = -self.MAX_Y_SPEED

        xp, yp, xvp, yvp = self.attempt_move(
            self.x, self.y, self.x_velocity, self.y_velocity
        )
        self.x = max(int(xp), 0)
        self.y = max(int(yp), 0)
        self.x_velocity = xvp
        self.y_velocity = yvp

    def draw(self, camera):
        pyxel.blt(
            self.x - camera.x,
            self.y - camera.y,
            self.IMG,
            self.IMG_ORIGIN_X,
            self.IMG_ORIGIN_Y,
            self.WIDTH,
            self.HEIGHT,
            0,
        )


class GemSparkle:
    ANIMATION_PERIOD = 6
    ANIMATION_DURATION = 12

    def __init__(self, x, y, sparkle_coordinates):
        self.x = x
        self.y = y
        self.u = sparkle_coordinates[0] * 8
        self.v = sparkle_coordinates[1] * 8

        self.animation_timer = 0
        self.is_dead = False

    def __str__(self):
        return (
            f"Sparkle: {self.x}, {self.y}, {self.u}, {self.v}, {self.animation_timer}"
        )

    def update(self):
        self.animation_timer += 1
        if self.animation_timer > self.ANIMATION_DURATION:
            self.is_dead = True

    def draw(self, camera):
        if (self.animation_timer % self.ANIMATION_PERIOD) < self.ANIMATION_PERIOD / 2.0:
            pyxel.blt(self.x - camera.x, self.y - camera.y, 0, self.u, self.v, 8, 8, 0)


class App:
    TITLE = 0
    PLAY = 1

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("obstacle.pyxres")

        # edit the FAKE_SMOKE image in memory so that it looks exactly like the real smoke
        smoke_color = pyxel.images[0].pget(REAL_SMOKE[0] * 8, REAL_SMOKE[1] * 8)
        for x in range(0, 8):
            for y in range(0, 8):
                pyxel.images[0].pset(
                    FAKE_SMOKE[0] * 8 + x, FAKE_SMOKE[1] * 8 + y, smoke_color
                )

        self.scene = self.TITLE
        pyxel.playm(msc=1, sec=0, loop=True)

        self.level = 1
        self.player = Player()
        self.camera = Camera(0, 0, self.player)
        self.tilemap = Tilemap(0, 0, 0, 256 * 8, 256 * 8, 0)
        self.tilemap.load_tilemap()
        self.player.x, self.player.y = self.tilemap.starting_tiles[self.level]
        self.sparkles = []
        pyxel.run(self.update, self.draw)

    def start_level(self):
        self.player.x, self.player.y = self.tilemap.starting_tiles[self.level]
        self.player.x_velocity = 0
        self.player.y_velocity = 0
        if self.level == 28:
            pyxel.playm(msc=2, sec=0, loop=True)

    def update(self):
        if self.scene == self.TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.playm(msc=0, sec=0, loop=True)
                self.scene = self.PLAY
        elif self.scene == self.PLAY:
            self.player.update()
            self.camera.update()
            for sparkle in self.sparkles:
                sparkle.update()
                if sparkle.is_dead:
                    self.sparkles.remove(sparkle)

            intersecting_tiles = self.player.intersecting_tiles(
                self.player.x, self.player.y
            )
            for tile in intersecting_tiles:
                if tile == NEXT_LEVEL_BLOCK:
                    self.player.next_level = True
                    break

                if tile in DANGER_BLOCKS:
                    self.player.kill()
                    break

                if tile == REPLACEMENT_GEM_BLOCK:
                    # TODO: handle gem behavior
                    shortest_distance = 50
                    matching_gem = None
                    for gem in self.tilemap.gems:
                        xd = self.player.x - gem[0][0]
                        yd = self.player.y - gem[0][1]
                        rough_distance = xd * xd + yd * yd
                        shortest_distance = min(shortest_distance, rough_distance)
                        if rough_distance == shortest_distance:
                            matching_gem = gem
                    if matching_gem:
                        self.tilemap.gems.remove(matching_gem)
                        pyxel.tilemaps[0].pset(
                            matching_gem[0][0] / 8, matching_gem[0][1] / 8, ALL_BLACK
                        )
                        self.sparkles.append(
                            GemSparkle(
                                matching_gem[0][0],
                                matching_gem[0][1],
                                GEMS[matching_gem[1]],
                            )
                        )
                        pyxel.play(1, 19)

            bottom_tiles = self.player.bottom_tiles(self.player.x, self.player.y)
            for tile in bottom_tiles:
                if tile in DANGER_FROM_BELOW_BLOCKS:
                    self.player.kill()
                    break

            top_tiles = self.player.top_tiles(self.player.x, self.player.y)
            for tile in top_tiles:
                if tile in DANGER_FROM_ABOVE_BLOCKS:
                    self.player.kill()
                    break

            if pyxel.btnp(pyxel.KEY_RIGHTBRACKET):
                self.level += 1
                self.start_level()
            elif pyxel.btnp(pyxel.KEY_LEFTBRACKET):
                self.level -= 1
                self.start_level()

            if self.player.next_level:
                self.level += 1
                self.start_level()
                self.player.next_level = False

            if self.player.is_dead:
                self.start_level()
                self.player.is_dead = False

    def draw_title_word(self, initial_y, initial_v, num_letters):
        letter_width = 16
        letter_height = 16
        padding = 3
        word_width = (letter_width + padding) * num_letters - padding
        u = 0
        v = initial_v
        x = (pyxel.width - word_width) / 2
        y = initial_y
        for i in range(0, 8):
            pyxel.blt(x, y, 0, u, v, letter_width, letter_height)
            x += letter_width + padding
            u += letter_width

    def draw(self):
        pyxel.cls(0)
        if self.scene == self.TITLE:
            self.draw_title_word(initial_y=10, initial_v=48, num_letters=8)
            self.draw_title_word(initial_y=36, initial_v=64, num_letters=5)
            pyxel.text(40, 80, "Press SPACE to play", 9)
        elif self.scene == self.PLAY:
            pyxel.bltm(0, 0, 0, self.camera.x, self.camera.y, pyxel.width, pyxel.height)
            for gem in self.tilemap.gems:
                x = gem[0][0] - self.camera.x
                y = gem[0][1] - self.camera.y
                u = gem[1][0] * 8
                v = gem[1][1] * 8
                pyxel.blt(x, y, 0, u, v, 8, 8, 0)
            for sparkle in self.sparkles:
                sparkle.draw(self.camera)
            self.player.draw(self.camera)


App()
