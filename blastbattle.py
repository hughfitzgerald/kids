import pyxel

SCREEN_HEIGHT = 120
SCREEN_WIDTH = 160

METEOR_SCORE = 10


class SoundBank:
    SHIP_DAMAGE_SOUND = 0
    METEOR_DAMAGE_SOUND = 2
    SHOOT_SOUND = 4


class Collider:
    IMG: int
    IMG_ORIGIN_X: int
    IMG_ORIGIN_Y: int
    WIDTH: int
    HEIGHT: int
    SPEED: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_alive = True

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

    def is_collide(self, other: Collider):
        return (
            self.x < other.x + other.WIDTH
            and self.x + self.WIDTH > other.x
            and self.y < other.y + other.HEIGHT
            and self.y + self.HEIGHT > other.y
        )


class Ship(Collider):
    IMG = 0
    IMG_ORIGIN_X = 0
    IMG_ORIGIN_Y = 0
    WIDTH = 3
    HEIGHT = 3
    SPEED = 1

    def __init__(self):
        super().__init__(
            x=pyxel.width / 2 - self.WIDTH / 2,
            y=pyxel.height - self.HEIGHT - pyxel.height / 12,
        )

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x -= self.SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x += self.SPEED
        self.x = max(0, min(self.x, pyxel.width - self.WIDTH))


class Meteor(Collider):
    IMG = 0
    IMG_ORIGIN_X = 1
    IMG_ORIGIN_Y = 8
    WIDTH = 6
    HEIGHT = 9
    SPEED = 2

    def __init__(self):
        starting_position = pyxel.rndi(1, 3)
        if starting_position == 1:
            self.x = pyxel.width / 16
        elif starting_position == 2:
            self.x = pyxel.width / 2 - self.WIDTH / 2
        else:
            self.x = pyxel.width - self.WIDTH - pyxel.width / 16
        self.y = 0 - self.HEIGHT
        self.is_exploded = False
        super().__init__(x=self.x, y=self.y)

    def update(self):
        self.y += self.SPEED
        if self.y > pyxel.height:
            self.is_alive = False

    def draw(self):
        super().draw()
        if self.is_exploded:
            pyxel.rect(self.x, self.y, 1, 1, 6)


class Bullet(Collider):
    WIDTH = 1
    HEIGHT = 1
    SPEED = 1
    COLOR = 8

    def draw(self):
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, self.COLOR)

    def update(self):
        self.y -= self.SPEED
        if self.y < 0:
            self.is_alive = False
        if self.y == pyxel.height / 4:
            self.is_alive = False


class Sparkle(Collider):
    IMG = 0
    IMG_ORIGIN_X = 3
    IMG_ORIGIN_Y = 0
    HEIGHT = 3
    WIDTH = 3


class Explosion(Collider):
    IMG = 0
    IMG_ORIGIN_X = 8
    IMG_ORIGIN_Y = 0
    WIDTH = 7
    HEIGHT = 7
    DURATION = 50

    def __init__(self, x, y):
        super().__init__(x - self.WIDTH / 2, y - self.HEIGHT / 2)
        self.time = 0

    def update(self):
        self.time += 1
        if self.time > self.DURATION:
            self.is_alive = False

    def draw(self):
        super().draw()

        if self.time % 16 > 4:
            Sparkle(self.x - 4, self.y + 2).draw()
            Sparkle(self.x + 2, self.y - 4).draw()
            Sparkle(self.x + self.WIDTH + 1, self.y + 2).draw()
            Sparkle(self.x + 2, self.y + self.HEIGHT + 1).draw()


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
                pyxel.play(0, SoundBank.METEOR_DAMAGE_SOUND)

        if not self.meteor.is_exploded and self.meteor.is_collide(self.ship):
            self.score -= METEOR_SCORE
            pyxel.play(0, SoundBank.SHIP_DAMAGE_SOUND)
            self.meteor.is_exploded = True

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.quit()

        self.ship.update()

        if (
            pyxel.btn(pyxel.KEY_SPACE)
            or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
            or pyxel.btnp(pyxel.KEY_M)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)
        ):
            self.bullets.append(Bullet(self.ship.x + 1, self.ship.y - 1))
            pyxel.play(0, SoundBank.SHOOT_SOUND)

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

        pyxel.text(pyxel.width * 9 / 16, 5, f"SCORE: {self.score:08d}", 7)


App()
