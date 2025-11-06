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


class Room:
    def __init__(self):
        self.inventory = {}
        self.targets = {}
        self.data = {}
        self.paths = {}

    def look(self):
        print("You look around.")
        for target in self.targets:
            if target == "hole":
                print("There's a hole in the wall!")
            elif target == "tree":
                print("There's a beautiful tree you planted!")
            elif target == "dirt":
                print("There's dirt on the ground.")
        for item in self.inventory:
            print(f"You see a {item}.")

    def use(self, inventory, item, target):
        if target in self.targets:
            print(f"You use the {item} on the {target}.")
            if item == "block" and target == "hole":
                print("You fixed the hole in the wall!")
                print("You win the game!")
                inventory.discard("block")
                self.targets.discard("hole")
                hole_in_the_wall = False
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
            else:
                print("Nothing happened.")
        else:
            print(f"There's no {target}.")

    def move(self, direction):
        if direction in self.paths:
            return self.paths[direction]
        else:
            print("You can't go that way.")
            return self


class Game:
    def __init__(self):
        self.inventory = {"tree-seed", "shovel"}

        OVERWORLD = Room()
        LAVA_PIT = Room()
        END = Room()
        self.current_room = OVERWORLD

        OVERWORLD.inventory = {"key"}
        OVERWORLD.targets = {
            "crafting-table": {"look": ["You can craft something."]},
            "door": {
                "locked": True,
                "look": {
                    "locked": {
                        True: "You see a big metal door. It's locked",
                        False: "You see a big metal door. It's unlocked.",
                    }
                },
            },
        }
        OVERWORLD.paths = {"south": LAVA_PIT}

        LAVA_PIT.inventory = {
            "peanut",
            "apple",
            "block-one",
            "block-two",
            "block-three",
        }
        LAVA_PIT.targets = {"lava"}
        LAVA_PIT.paths = {"north": OVERWORLD, "south": END}

        END.inventory = {"block", "scooter", "broken-torch"}
        END.targets = {"hole", "dirt"}
        END.paths = {"north": LAVA_PIT}

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
                    self.current_room.look()
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


Game().run()
