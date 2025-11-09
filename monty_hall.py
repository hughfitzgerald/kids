import random


def monty_hall(strategy="switch"):
    prize = int(random.random() * 3) + 1
    initial_choice = 1
    if strategy == "switch":
        if prize == 2:
            he_opens = 3
            new_choice = 2
        else:
            he_opens = 2
            new_choice = 3
    if strategy == "stay":
        new_choice = 1
    if new_choice == prize:
        return True
    else:
        return False


switch_wins = 0
stay_wins = 0
number_of_games = 9000
for i in range(number_of_games):
    if monty_hall("switch"):
        switch_wins += 1
    if monty_hall("stay"):
        stay_wins += 1
print(f"Always switching wins {100.0 * switch_wins / number_of_games}% of the time")
print(f"Always staying wins {100.0 * stay_wins / number_of_games}% of the time")
