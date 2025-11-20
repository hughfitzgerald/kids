import random
import sys


def monty_hall(strategy="switch"):
    prize = int(random.random() * 3) + 1
    choice = 1
    if strategy == "switch":
        if prize == 2:
            # he_opens = 3
            choice = 2
        else:
            # he_opens = 2
            choice = 3
    if strategy == "stay":
        choice = 1
    if choice == prize:
        return True
    else:
        return False


def monte_carlo(number_of_games=1000):
    switch_wins = 0
    stay_wins = 0
    for i in range(number_of_games):
        if monty_hall("switch"):
            switch_wins += 1
        if monty_hall("stay"):
            stay_wins += 1
    switch_win_percentage = 100.0 * switch_wins / number_of_games
    stay_win_percentage = 100.0 * stay_wins / number_of_games

    print(f"Always switching wins {switch_win_percentage}% of the time")
    print(f"Always staying wins {stay_win_percentage}% of the time")

    if switch_win_percentage > stay_win_percentage:
        print("Switching is the better strategy.")
    elif stay_win_percentage > switch_win_percentage:
        print("Staying is the better strategy.")
    else:
        print("Both strategies are equally good.")


if __name__ == "__main__":
    number_of_games = 1000
    if len(sys.argv) > 1:
        number_of_games = int(sys.argv[1])

    monte_carlo(number_of_games)
