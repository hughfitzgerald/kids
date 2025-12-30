from abc import ABC, abstractmethod
import json


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
        self.recording_queue = CommandQueue()
        self.playback = False
        self.playback_queue = CommandQueue()

    def update(self):
        if self.recording or self.playback:
            self.timer += 1
        if self.playback:
            if self.playback_queue.queue:
                while (
                    self.playback_queue.queue
                    and self.playback_queue.queue[0][0] == self.timer
                ):
                    command = self.playback_queue.pop_command()[1]
                    self.execute(command)
            else:
                self.playback = False

    def start_recording(self):
        self.timer = 0
        self.recording = True

    def stop_recording(self):
        self.timer = 0
        self.recording = False
        self.recording_queue.serialize("data.json")

    def start_playback(self):
        self.timer = 0
        self.playback = True
        self.playback_queue = CommandQueue.deserialize("data.json")

    def execute(self, command):
        command(self.player).execute()
        if self.recording:
            self.recording_queue.add_command(self.timer, command)


class CommandQueue:
    def __init__(self):
        self.queue = []

    def add_command(self, timer, command):
        self.queue.append((timer, command))
        self.queue.sort(key=lambda x: x[0])

    def pop_command(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def to_list(self):
        self.queue.sort(key=lambda x: x[0])
        return [(timer, command.__name__) for timer, command in self.queue]

    def serialize(self, filename):
        with open(filename, "w") as file:
            json.dump(self.to_list(), file)

    @staticmethod
    def deserialize(filename):
        with open(filename, "r") as file:
            data = json.load(file)
        command_queue = CommandQueue()
        for timer, command_name in data:
            command = globals().get(command_name)
            if command:
                command_queue.add_command(timer, command)
        return command_queue
