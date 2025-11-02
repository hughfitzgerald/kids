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

inventory = {"tree-seed", "shovel"}
room_inventory = {"block", "scooter", "broken-torch"}
room_targets = {"hole", "dirt"}

while True:
    command = input("What do you want to do? ")
    match command.split():
        case ["pickup", item]:
            if item in room_inventory:
                print(f"You picked up the {item}.")
                inventory.add(item)
                room_inventory.discard(item)
            else:
                print(f"There's no {item} in the room.")
        case ["drop", item]:
            if item in inventory:
                print(f"You dropped the {item}.")
                inventory.discard(item)
                room_inventory.add(item)
            else:
                print(f"There's no {item} in your inventory.")
        case ["look"]:
            print("You look around.")
            for target in room_targets:
                if target == "hole":
                    print("There's a hole in the wall!")
                elif target == "tree":
                    print("There's a beautiful tree you planted!")
                elif target == "dirt":
                    print("There's dirt on the ground.")
            for item in room_inventory:
                print(f"You see a {item}.")
        case ["inventory"]:
            print("You check your inventory.")
            for item in inventory:
                print(f"You see a {item}.")
        case ["use", item, "on", target]:
            if item in inventory:
                if target in room_targets:
                    print(f"You use the {item} on the {target}.")
                    if item == "block" and target == "hole":
                        print("You used the block to fix the hole in the wall.")
                        print("You win the game!")
                        inventory.discard("block")
                        room_targets.discard("hole")
                        hole_in_the_wall = False
                        break
                    elif item == "tree-seed" and target == "dirt":
                        print("You planted a tree and it grew!")
                        inventory.discard("tree-seed")
                        room_targets.discard("dirt")
                        room_targets.add("tree")
                    else:
                        print("Nothing happened.")
                else:
                    print(f"There's no {target}.")
            else:
                print(f"You don't have {item} in your inventory.")
        case ["quit"]:
            print("Goodbye!")
            break
