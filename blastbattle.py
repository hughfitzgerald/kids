import pyxel

SCREEN_HEIGHT = 120
SCREEN_WIDTH = 160

SHIP_WIDTH = 3
SHIP_HEIGHT = 3
SHIP_SPEED = 1

EXPLOSION_TIME = 50
EXPLOSION_WIDTH = 7
EXPLOSION_HEIGHT = 7


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
        pyxel.blt(self.x, self.y, 0, 8, 0, EXPLOSION_WIDTH, EXPLOSION_HEIGHT)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("blastbattle.pyxres")
        self.ship_x = SCREEN_WIDTH / 2
        self.ship_y = SCREEN_HEIGHT - SHIP_HEIGHT - 10
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

        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.ship_x, self.ship_y, 0, 0, 0, SHIP_WIDTH, SHIP_HEIGHT)
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


App()
