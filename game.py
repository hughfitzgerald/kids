# what_they_typed_in = input("Do you go doodoo?")

# if what_they_typed_in == "I go doodoo!":
#     print("Me go doodoo too!")
# else:
#     print("That's not necessary!")

# what_they_typed_in = input("Glasses or eyes?")

# if what_they_typed_in == "glasses, eyes":
#     print("I'm saying 'glasses, eyes' too!")
# else:
#     print("Chicken bock!")

# maris_favorite_things = ["pokemon cards", "video games", "soccer", "family", "movies"]
# number_of_the_last_thing = len(maris_favorite_things) - 1
# for thing in maris_favorite_things:
#     if thing is maris_favorite_things[number_of_the_last_thing]:
#         print("AND...")
#     print(f"I love {thing}!")
import random


class Character:
    def __init__(self, name="", current_room=None):
        self.name = name
        self.current_room = current_room

    def move(self):
        random_number = int(random.random() * 4) + 1
        if random_number == 1:
            direction = "north"
        elif random_number == 2:
            direction = "east"
        elif random_number == 3:
            direction = "west"
        else:
            direction = "south"
        if direction in self.current_room.paths:
            new_room = self.current_room.paths[direction]["destination"]
            print(
                f"{self.name} moved {direction} from {self.current_room.name} to {new_room.name} because he can walk through walls."
            )
            self.current_room = new_room


class Room:
    def __init__(self, name="", inventory={}, targets={}, data={}, paths={}):
        self.name = name
        self.inventory = inventory
        self.targets = targets
        self.data = data
        self.paths = paths
        self.win = False

    def look(self, characters):
        print("You look around.")
        for target in self.targets:
            print(f"You see a {target}.")
        for item in self.inventory:
            print(f"You see a {item}.")
        for character in characters:
            if character.current_room == self:
                print(f"You see {character.name}")

    def use(self, inventory, item, target):
        if target in self.targets:
            print(f"You use the {item} on the {target}.")
            if item == "block" and target == "hole":
                print("You fixed the hole in the wall!")
                inventory.discard("block")
                self.targets.discard("hole")
                self.win = True
                return
            elif item == "tree-seed" and target == "dirt":
                print("You planted a tree and it grew!")
                inventory.discard("tree-seed")
                self.targets.discard("dirt")
                self.targets.add("tree")
            elif "block" in item and target == "lava":
                if "blocks" not in self.data:
                    self.data["blocks"] = set()
                print(f"You threw the {item} in the lava and it floats!")
                self.data["blocks"].add(item)
                if (
                    "block-one" in self.data["blocks"]
                    and "block-two" in self.data["blocks"]
                    and "block-three" in self.data["blocks"]
                ):
                    self.paths["south"]["locked"] = False
                    print("You made a bridge with the blocks, they float in the lava.")
            elif item == "key" and target == "door":
                self.paths["south"]["locked"] = False
                print("You unlocked the door!")
            elif item == "broken-key" and target == "crafting-table":
                print("You fixed the key!")
                inventory.discard("broken-key")
                inventory.add("key")
            else:
                print("Nothing happened.")
        else:
            print(f"There's no {target}.")

    def move(self, direction):
        if direction in self.paths:
            if self.paths[direction].get("locked", False):
                print(self.paths[direction]["locked_message"])
                return self
            return self.paths[direction]["destination"]
        else:
            print("You can't go that way.")
            return self


class Game:
    def __init__(self):
        self.inventory = {"tree-seed", "shovel"}

        OVERWORLD = Room(
            name="Overworld",
            inventory={"broken-key"},
            targets={"crafting-table", "door"},
        )
        LAVA_PIT = Room(
            name="Lava Pit",
            inventory={"peanut", "apple", "block-one", "block-two", "block-three"},
            targets={"lava"},
        )
        END = Room(
            name="End Room",
            inventory={"block", "scooter", "broken-torch"},
            targets={"hole", "dirt"},
        )
        self.current_room = OVERWORLD

        OVERWORLD.paths = {
            "south": {
                "destination": LAVA_PIT,
                "locked": True,
                "locked_message": "You try to go through the door, but it's locked.",
            }
        }
        LAVA_PIT.paths = {
            "north": {"destination": OVERWORLD},
            "south": {
                "destination": END,
                "locked": True,
                "locked_message": "You died in the lava and you respawn back in the lava pit.",
            },
        }
        END.paths = {"north": {"destination": LAVA_PIT}}

        CLOREN = Character(name="Cloren", current_room=OVERWORLD)
        self.characters = {CLOREN}

    def run(self):
        while True:
            command = input("What do you want to do? ")
            match command.split():
                case ["pickup", item]:
                    if item in self.current_room.inventory:
                        print(f"You picked up the {item}.")
                        self.inventory.add(item)
                        self.current_room.inventory.discard(item)
                    else:
                        print(f"There's no {item} in the room.")
                case ["drop", item]:
                    if item in self.inventory:
                        print(f"You dropped the {item}.")
                        self.inventory.discard(item)
                        self.current_room.inventory.add(item)
                    else:
                        print(f"There's no {item} in your inventory.")
                case ["look"]:
                    self.current_room.look(self.characters)
                case ["inventory"]:
                    print("You check your inventory.")
                    for item in self.inventory:
                        print(f"You see a {item}.")
                case ["use", item, "on", target]:
                    if item in self.inventory:
                        self.current_room.use(self.inventory, item, target)
                    else:
                        print(f"You don't have {item} in your inventory.")
                case ["walk", direction]:
                    new_room = self.current_room.move(direction)
                    if new_room is not self.current_room:
                        self.current_room = new_room
                        print(f"You walk {direction}.")
                case ["quit"]:
                    print("Goodbye!")
                    break
            if self.current_room.win:
                print("You win the game!")
                print("Congratulations! Goodbye!")
                break
            for character in self.characters:
                character.move()


Game().run()
