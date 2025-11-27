import pyxel
from enum import IntEnum


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
        self.action_time_tick = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.x -= Player.SPEED
        elif pyxel.btn(pyxel.KEY_D):
            self.x += Player.SPEED

        if self.action != "static":
            if self.action_time_tick >= 10:
                self.action = "static"
                self.action_time_tick = 0
            else:
                self.action_time_tick += 1
        else:
            if pyxel.btnp(pyxel.KEY_J):
                self.action = "punch"
            if pyxel.btnp(pyxel.KEY_L):
                self.action = "kick"
            if pyxel.btnp(pyxel.KEY_I):
                self.action = "headbutt"

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
    class Screen(IntEnum):
        START = 0
        PLAY = 1

    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("rapid.pyxres")
        self.player = Player()
        self.screen = App.Screen.START
        self.intro_music_played = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.screen == App.Screen.START:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.screen = App.Screen.PLAY
            if not self.intro_music_played:
                pyxel.play(0, 0)
                self.intro_music_played = True
        elif self.screen == App.Screen.PLAY:
            self.player.update()

    def draw(self):
        pyxel.cls(0)
        if self.screen == App.Screen.PLAY:
            self.player.draw()
        if self.screen == App.Screen.START:
            title = "RAPID"
            welcome = "Welcome back!"
            directions = "Press SPACEBAR to start"
            character_width = 4
            line_height = 10
            pyxel.text(
                pyxel.width / 2 - (len(title) * character_width) / 2,
                pyxel.height / 3,
                title,
                7,
            )
            pyxel.text(
                pyxel.width / 2 - (len(welcome) * character_width) / 2,
                pyxel.height / 3 + line_height,
                welcome,
                7,
            )
            pyxel.text(
                pyxel.width / 2 - (len(directions) * character_width) / 2,
                pyxel.height / 3 + line_height * 2,
                directions,
                7,
            )


App()
