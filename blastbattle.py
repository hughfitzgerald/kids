import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("blastbattle.pyxres")
        self.ship_x = 80
        self.ship_y = 110
        self.bullets = []
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship_x -= 1

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship_x += 1

        if pyxel.btn(pyxel.KEY_SPACE):
            self.bullets.append({"x": self.ship_x + 1, "y": self.ship_y - 1})

        for bullet in self.bullets:
            bullet["y"] -= 1

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.ship_x, self.ship_y, 0, 0, 0, 3, 3)
        for bullet in self.bullets:
            pyxel.rect(bullet["x"], bullet["y"], 1, 1, 8)


App()
