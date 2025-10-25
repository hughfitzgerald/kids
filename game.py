what_they_typed_in = input("Do you go doodoo?")

if what_they_typed_in == "I go doodoo!":
    print("Me go doodoo too!")
else:
    print("That's not necessary!")

what_they_typed_in = input("Glasses or eyes?")

if what_they_typed_in == "glasses, eyes":
    print("I'm saying 'glasses, eyes' too!")
else:
    print("Chicken bock!")

maris_favorite_things = ["pokemon cards", "video games", "soccer", "family", "movies"]
number_of_the_last_thing = len(maris_favorite_things) - 1
for thing in maris_favorite_things:
    if thing is maris_favorite_things[number_of_the_last_thing]:
        print("AND...")
    print(f"I love {thing}!")
