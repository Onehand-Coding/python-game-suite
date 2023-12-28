import random
import math
import time
import sys


def Play_again():
    playAgain = ""
    print("\nDo you want to play again?(Y/n)")
    while playAgain not in ("Y", "N"):
        playAgain = input("> ").upper()
        if playAgain == "Y":
            print("\nOk, Let's play again!")
            time.sleep(1)
            guessMyNumber()
    print("\nOk Bye, see you next time!")
    sys.exit()


def play():
    print("Welcome to my Number Guessing Game!")
    print("\nSet lower bound and upper bound before you can start guessing.")
    time.sleep(1)
    print("\nStart? (Y/n)")
    time.sleep(1)

    start = ""
    while start not in ("Y", "N"):
        start = input('> ').upper()
        if start == "Y":
            print("\nLet's go!")
            guessMyNumber()

    print("Ok, maybe next time.")
    sys.exit()


def getBounds():
    print("\nSet  lower bound")
    while True:
        lower = input("> ")
        if not lower.isdigit():
            continue
        break
    lower = int(lower)

    print("Set upper bound ")
    while True:
        upper = input("> ")
        if not upper.isdigit():
            continue
        if int(upper) <= lower:
            print('Enter a number higher than your lower bound.')
            continue
        break
    upper = int(upper)

    return lower, upper


def guessMyNumber():
    time.sleep(1)
    used_numbers = []
    count = 0
    lowerBound, upperBound = getBounds()
    chances = round(math.log(upperBound - lowerBound + 1, 2))
    secret_num = random.randint(lowerBound, upperBound)

    while chances != 0:
        count += 1
        print("\nNumbers used:", ','.join(used_numbers))
        print(f"Chances left: {chances}")
        print("\nEnter your Guess:")
        try:
            guess = int(input("> "))
        except ValueError:
            print("\nEnter an Integer!")
            continue

        if str(guess) in used_numbers:
            print(f"\nnumber {guess} already used!")
            continue

        elif guess == secret_num:
            print(f"\nCongrats you guessed the number in {count} guesses with {chances} chances left!")
            break

        elif guess > secret_num:
            print("\nYou guessed too high!")

        elif guess < secret_num:
            print("\nYou guessed too low!")

        chances -= 1
        used_numbers.append(str(guess))

    if chances == 0:
        print(f"\nSorry you lost! the number was {secret_num} ")

    Play_again()


if __name__ == '__main__':
    print('press ctrl + c to quit')
    print()
    try:
        play()
    except KeyboardInterrupt:
        print('Bye, Thanks for playing!')
        sys.exit()
