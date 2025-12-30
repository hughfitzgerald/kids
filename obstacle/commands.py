from abc import ABC, abstractmethod
import pickle


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class MoveRightCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.move_right()


class MoveLeftCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.move_left()


class JumpCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.jump()


class PunchCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        self.player.punch()


class CommandManager:
    def __init__(self, player):
        self.timer = 0
        self.player = player
        self.recording = False
        self.recording_queue = []
        self.playback = False
        self.playback_queue = []

    def update(self):
        if self.recording or self.playback:
            self.timer += 1
        if self.playback:
            if self.playback_queue:
                if self.playback_queue[0][0] == self.timer:
                    command = self.playback_queue.pop(0)[1]
                    self.execute(command)
            else:
                self.playback = False

    def start_recording(self):
        self.timer = 0
        self.recording = True

    def stop_recording(self):
        self.timer = 0
        self.recording = False
        with open("data.pkl", "wb") as file:
            pickle.dump(self.recording_queue, file)

    def start_playback(self):
        self.timer = 0
        self.playback = True
        with open("data.pkl", "rb") as file:
            self.playback_queue = pickle.load(file)

    def execute(self, command):
        command(self.player).execute()
        if self.recording:
            self.recording_queue.append((self.timer, command))
