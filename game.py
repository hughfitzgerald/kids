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

    def use(self, item, target):
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


OVERWORLD = Room()

LAVA_PIT = Room()
LAVA_PIT.inventory = {"peanut", "apple", "block-one", "block-two", "block-three"}
LAVA_PIT.targets = {"lava"}

END = Room()
END.inventory = {"block", "scooter", "broken-torch"}
END.targets = {"hole", "dirt"}

LAVA_PIT.paths = {"north": OVERWORLD, "south": END}

inventory = {"tree-seed", "shovel"}

while True:
    command = input("What do you want to do? ")
    match command.split():
        case ["pickup", item]:
            if item in END.inventory:
                print(f"You picked up the {item}.")
                inventory.add(item)
                END.inventory.discard(item)
            else:
                print(f"There's no {item} in the room.")
        case ["drop", item]:
            if item in inventory:
                print(f"You dropped the {item}.")
                inventory.discard(item)
                END.inventory.add(item)
            else:
                print(f"There's no {item} in your inventory.")
        case ["look"]:
            END.look()
        case ["inventory"]:
            print("You check your inventory.")
            for item in inventory:
                print(f"You see a {item}.")
        case ["use", item, "on", target]:
            if item in inventory:
                END.use(item, target)
            else:
                print(f"You don't have {item} in your inventory.")
        case ["quit"]:
            print("Goodbye!")
            break
