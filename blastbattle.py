import pyxel

SCREEN_HEIGHT = 120
SCREEN_WIDTH = 160

SHIP_ORIGIN_X = 0
SHIP_ORIGIN_Y = 0
SHIP_WIDTH = 3
SHIP_HEIGHT = 3
SHIP_SPEED = 1

EXPLOSION_ORIGIN_X = 8
EXPLOSION_ORIGIN_Y = 0
EXPLOSION_TIME = 50
EXPLOSION_WIDTH = 7
EXPLOSION_HEIGHT = 7

SPARKLE_ORIGIN_X = 3
SPARKLE_ORIGIN_Y = 0
SPARKLE_HEIGHT = 3
SPARKLE_WIDTH = 3

METEOR_WIDTH = 6
METEOR_HEIGHT = 9
METEOR_ORIGIN_X = 1
METEOR_ORIGIN_Y = 8
METEOR_SPEED = 2
METEOR_SCORE = 10


class Meteor:
    def __init__(self):
        self.is_alive = True
        self.is_exploded = False
        starting_position = pyxel.rndi(1, 3)
        if starting_position == 1:
            self.x = 10
        elif starting_position == 2:
            self.x = SCREEN_WIDTH / 2
        else:
            self.x = SCREEN_WIDTH - METEOR_WIDTH - 10
        self.y = 0 - METEOR_HEIGHT

    def update(self):
        self.y += METEOR_SPEED
        if self.y > SCREEN_HEIGHT:
            self.is_alive = False

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            METEOR_ORIGIN_X,
            METEOR_ORIGIN_Y,
            METEOR_WIDTH,
            METEOR_HEIGHT,
        )
        if self.is_exploded:
            pyxel.rect(self.x, self.y, 1, 1, 6)

    def is_collide(self, x, y):
        if self.is_exploded:
            return False
        if (
            x >= self.x
            and x < self.x + METEOR_WIDTH
            and y >= self.y
            and y < self.y + METEOR_HEIGHT
        ):
            return True
        else:
            return False


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        self.is_alive = True

    def update(self):
        self.time += 1
        if self.time > EXPLOSION_TIME:
            self.is_alive = False

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            EXPLOSION_ORIGIN_X,
            EXPLOSION_ORIGIN_Y,
            EXPLOSION_WIDTH,
            EXPLOSION_HEIGHT,
        )

        if self.time % 16 > 4:
            pyxel.blt(
                self.x - 4,
                self.y + 2,
                0,
                SPARKLE_ORIGIN_X,
                SPARKLE_ORIGIN_Y,
                SPARKLE_WIDTH,
                SPARKLE_HEIGHT,
            )
            pyxel.blt(
                self.x + 2,
                self.y - 4,
                0,
                SPARKLE_ORIGIN_X,
                SPARKLE_ORIGIN_Y,
                SPARKLE_WIDTH,
                SPARKLE_HEIGHT,
            )
            pyxel.blt(
                self.x + EXPLOSION_WIDTH + 1,
                self.y + 2,
                0,
                SPARKLE_ORIGIN_X,
                SPARKLE_ORIGIN_Y,
                SPARKLE_WIDTH,
                SPARKLE_HEIGHT,
            )
            pyxel.blt(
                self.x + 2,
                self.y + EXPLOSION_WIDTH + 1,
                0,
                SPARKLE_ORIGIN_X,
                SPARKLE_ORIGIN_Y,
                SPARKLE_WIDTH,
                SPARKLE_HEIGHT,
            )


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("blastbattle.pyxres")
        self.score = 0
        self.ship_x = SCREEN_WIDTH / 2
        self.ship_y = SCREEN_HEIGHT - SHIP_HEIGHT - 10
        self.meteor = Meteor()
        self.bullets = []
        self.explosions = []
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship_x -= SHIP_SPEED

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship_x += SHIP_SPEED

        self.ship_x = max(self.ship_x, 0)
        self.ship_x = min(self.ship_x, SCREEN_WIDTH - SHIP_WIDTH)

        if pyxel.btn(pyxel.KEY_SPACE):
            self.bullets.append({"x": self.ship_x + 1, "y": self.ship_y - 1})

        if pyxel.btnp(pyxel.KEY_M):
            self.bullets.append({"x": self.ship_x + 1, "y": self.ship_y - 1})

        if not self.meteor.is_alive:
            self.meteor = Meteor()
        else:
            self.meteor.update()

        for bullet in self.bullets:
            bullet["y"] -= 1
            if bullet["y"] == 30:
                self.explosions.append(
                    Explosion(
                        bullet["x"] - EXPLOSION_WIDTH / 2,
                        bullet["y"] - EXPLOSION_HEIGHT / 2,
                    )
                )
                self.bullets.remove(bullet)
            elif self.meteor.is_collide(bullet["x"], bullet["y"]):
                self.explosions.append(
                    Explosion(
                        bullet["x"] - EXPLOSION_WIDTH / 2,
                        bullet["y"] - EXPLOSION_HEIGHT / 2,
                    )
                )
                self.meteor.is_exploded = True
                self.bullets.remove(bullet)
                self.score += METEOR_SCORE

        if (
            self.meteor.is_collide(self.ship_x, self.ship_y)
            or self.meteor.is_collide(self.ship_x + SHIP_WIDTH - 1, self.ship_y)
            or self.meteor.is_collide(self.ship_x, self.ship_y + SHIP_HEIGHT - 1)
            or self.meteor.is_collide(
                self.ship_x + SHIP_WIDTH - 1, self.ship_y + SHIP_HEIGHT - 1
            )
        ):
            self.score -= METEOR_SCORE
            self.meteor.is_exploded = True

        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(
            self.ship_x,
            self.ship_y,
            0,
            SHIP_ORIGIN_X,
            SHIP_ORIGIN_Y,
            SHIP_WIDTH,
            SHIP_HEIGHT,
        )
        for bullet in self.bullets:
            pyxel.rect(
                bullet["x"],
                bullet["y"],
                1,
                1,
                8,
            )

        for explosion in self.explosions:
            explosion.draw()

        if self.meteor.is_alive:
            self.meteor.draw()

        pyxel.text(SCREEN_WIDTH - 70, 5, f"SCORE: {self.score:08d}", 7)


App()
