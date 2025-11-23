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

SHIP_DAMAGE_SOUND = 0
METEOR_DAMAGE_SOUND = 2
SHOOT_SOUND = 4

BULLET_COLOR = 8
BULLET_SPEED = 1
BULLET_WIDTH = 1
BULLET_HEIGHT = 1


class Collider:
    def __init__(
        self, x: int, y: int, img: int, u: int, v: int, w: int, h: int, speed: int
    ):
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.speed = speed
        self.is_alive = True

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h)

    def is_collide(self, other: Collider):
        return (
            self.x < other.x + other.w
            and self.x + self.w > other.x
            and self.y < other.y + other.h
            and self.y + self.h > other.y
        )


class Ship(Collider):
    def __init__(self):
        super().__init__(
            x=pyxel.width / 2,
            y=pyxel.height - SHIP_HEIGHT - 10,
            img=0,
            u=SHIP_ORIGIN_X,
            v=SHIP_ORIGIN_Y,
            w=SHIP_WIDTH,
            h=SHIP_HEIGHT,
            speed=SHIP_SPEED,
        )

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x += self.speed
        self.x = max(0, min(self.x, pyxel.width - self.w))


class Meteor(Collider):
    def __init__(self):
        starting_position = pyxel.rndi(1, 3)
        if starting_position == 1:
            self.x = 10
        elif starting_position == 2:
            self.x = pyxel.width / 2
        else:
            self.x = pyxel.width - METEOR_WIDTH - 10
        self.y = 0 - METEOR_HEIGHT
        super().__init__(
            x=self.x,
            y=self.y,
            img=0,
            u=METEOR_ORIGIN_X,
            v=METEOR_ORIGIN_Y,
            w=METEOR_WIDTH,
            h=METEOR_HEIGHT,
            speed=METEOR_SPEED,
        )
        self.is_exploded = False

    def update(self):
        self.y += self.speed
        if self.y > pyxel.height:
            self.is_alive = False

    def draw(self):
        super().draw()
        if self.is_exploded:
            pyxel.rect(self.x, self.y, 1, 1, 6)


class Bullet(Collider):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            img=None,
            u=None,
            v=None,
            w=BULLET_WIDTH,
            h=BULLET_HEIGHT,
            speed=BULLET_SPEED,
        )

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.is_alive = False
        if self.y == 30:
            self.is_alive = False


class Explosion(Collider):
    def __init__(self, x, y):
        super().__init__(
            x - EXPLOSION_WIDTH / 2,
            y - EXPLOSION_HEIGHT / 2,
            0,
            EXPLOSION_ORIGIN_X,
            EXPLOSION_ORIGIN_Y,
            EXPLOSION_WIDTH,
            EXPLOSION_HEIGHT,
            0,
        )
        self.time = 0

    def update(self):
        self.time += 1
        if self.time > EXPLOSION_TIME:
            self.is_alive = False

    def draw(self):
        super().draw()

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
                self.x + self.w + 1,
                self.y + 2,
                0,
                SPARKLE_ORIGIN_X,
                SPARKLE_ORIGIN_Y,
                SPARKLE_WIDTH,
                SPARKLE_HEIGHT,
            )
            pyxel.blt(
                self.x + 2,
                self.y + self.h + 1,
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
        self.ship = Ship()
        self.meteor = Meteor()
        self.bullets = []
        self.explosions = []
        pyxel.run(self.update, self.draw)

    def detect_collisions(self):
        for bullet in self.bullets:
            if self.meteor.is_collide(bullet):
                self.explosions.append(Explosion(bullet.x, bullet.y))
                self.meteor.is_exploded = True
                self.bullets.remove(bullet)
                self.score += METEOR_SCORE
                pyxel.play(0, METEOR_DAMAGE_SOUND)

        if not self.meteor.is_exploded and self.meteor.is_collide(self.ship):
            self.score -= METEOR_SCORE
            pyxel.play(0, SHIP_DAMAGE_SOUND)
            self.meteor.is_exploded = True

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.quit()

        self.ship.update()

        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            self.bullets.append(Bullet(self.ship.x + 1, self.ship.y - 1))
            pyxel.play(0, SHOOT_SOUND)

        if pyxel.btnp(pyxel.KEY_M) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.bullets.append(Bullet(self.ship.x + 1, self.ship.y - 1))
            pyxel.play(0, SHOOT_SOUND)

        if not self.meteor.is_alive:
            self.meteor = Meteor()
        else:
            self.meteor.update()

        for bullet in self.bullets:
            bullet.update()
            if not bullet.is_alive:
                self.explosions.append(Explosion(bullet.x, bullet.y))
                self.bullets.remove(bullet)

        self.detect_collisions()

        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def draw(self):
        pyxel.cls(0)
        self.ship.draw()
        for bullet in self.bullets:
            bullet.draw()

        if self.meteor.is_alive:
            self.meteor.draw()

        for explosion in self.explosions:
            explosion.draw()

        pyxel.text(pyxel.width - 70, 5, f"SCORE: {self.score:08d}", 7)


App()
