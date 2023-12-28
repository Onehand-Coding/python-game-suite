import random
import time
import sys

WEAPONS = {
    "r": "rock",
    "p": "paper",
    "s": "scissors",
}


def play_again():
    print('play_again?(Y/n)')
    return input('> ').lower().startswith('y')


def getPlayerMove():
    while True:
        weapon = input("(R)rock,(P)aper, or (S)scissors?: ").lower()
        if weapon == 'q':
            print("Goodbye! see you again next time...")
            sys.exit()
        if weapon in WEAPONS:
            return WEAPONS.get(weapon)


def rpsg():
    player = ""
    player_score = 0
    computer_score = 0
    ties = 0
    rounds = 0
    print("\npress Q to quit \n")

    while True:
        rounds += 1
        computer = WEAPONS.get(random.choice(list(WEAPONS)))
        player = getPlayerMove()

        if player == computer:
            print("Computer: ", computer)
            print("Player: ", player)
            print("Tie!")
            ties += 1

        elif player == "rock" and computer == "scissors":
            print("computer: ", computer)
            print("player: ", player)
            print("You Win!")
            player_score += 1

        elif player == "paper" and computer == "rock":
            print("computer: ", computer)
            print("player: ", player)
            print("You Win!")
            player_score += 1

        elif player == "scissors" and computer == "paper":
            print("computer: ", computer)
            print("player: ", player)
            print("You Win!")
            player_score += 1

        else:
            print("computer: ", computer)
            print("player: ", player)
            print("you lose!")
            computer_score += 1

        if computer_score == 3 or player_score == 3:
            break

    print("-----------------------\n")

    if player_score > computer_score:
        print(f"You're in luck today, You won against the computer in {rounds} rounds\n")
    else:
        print(f"Better luck next time :) The Computer won in {rounds} rounds\n")
    print(f"Scores:\n\tyou: {player_score}\n\tcomputer: {computer_score}\n\tTies: {ties}")

    if play_again():
        rpsg()
    else:
        print('Bye, Thanks for playing!')


if __name__ == '__main__':
    print("Hello Welcome to my Rock, Paper, or Scissors Game!\nchoose your weapon wisely!..")
    time.sleep(1)
    rpsg()
