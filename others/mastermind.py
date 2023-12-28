import sys
import time
import random

FLAG = 0


def get_secret_num(flag):
    """Generates the secret number based in the current flag value."""
    if flag >= 9:
        return str(random.randrange(100000, 1000000))  # return 6-digit number
    elif flag >= 6:
        return str(random.randrange(10000, 100000))  # returns 5-digit number
    elif flag >= 3:
        return str(random.randrange(1000, 10000))  # returns 4-digit number
    elif flag >= 0:
        return str(random.randrange(100, 1000))  # returns 3-digit number


def play_again(flag):
    print("\nDo you want to play again? (Y/n)")
    play_again = None
    while play_again not in ("y", "n"):
        play_again = input("> ").lower()

        if play_again == "y":
            print("\nOk, let's go!")
            if flag >= 9:
                print("\nThis is the Hardest yet :)")
            elif flag == 6:
                print("\nThis will be harder I think :)")
            elif flag == 3:
                print("\nSeems easy for you,\nLet's add more fun :)")

            return True


def get_player_guess(secret_num):
    while True:
        guess_num = input("> ").lower()

        # if player wants to quit
        if guess_num == "q":
            print("Bye, Thanks for playing!")
            time.sleep(1)
            sys.exit()

        # Make sure player enters an integer and with same digit count as the secret number.
        if not guess_num.isdigit() or len(guess_num) != len(secret_num):
            print(f"\nEnter a {len(secret_num)}-digit number!")
            continue

        return guess_num


def there_is_match(secret_num, guess_num):
    return any(secret == guess for secret, guess in zip(secret_num, guess_num))


def matched(secret_num, guess_num):
    return all(secret == guess for secret, guess in zip(secret_num, guess_num))


def mastermind():
    global FLAG
    secret_number = get_secret_num(FLAG)
    player_lives = len(secret_number)
    player_guess = None
    rounds = 0

    print("\nGoodluck!")
    print('\n\t"Q" to quit!')
    print(f"\nGuess my {len(secret_number)}-digit number!")

    while player_lives and (player_guess != secret_number):
        rounds += 1
        player_guess = get_player_guess(secret_number)

        # Digit/'s matched from player guess and the secret number:
        if there_is_match(secret_number, player_guess):
            guess_hint = "".join(
                num if player_guess[i] == secret_number[i] else "X"
                for i, num in enumerate(secret_number)
            )
            correct_digits = [num.isdigit() for num in guess_hint].count(True)

            if correct_digits == 1:
                print(f"\nNot exactly my Number but you got a digit correct!", guess_hint)
            elif correct_digits > 1 and not matched(secret_number, player_guess):
                print(f"\nNot exactly my Number but you got {correct_digits} digits correct!", guess_hint)

        # No digit matched.
        else:
            player_lives -= 1
            print("\nNot a single digit matched!")
            if player_lives:
                print(f"\nYou have {player_lives} lives left.")

    # Player have guessed the secret number:
    if matched(secret_number, player_guess):
        FLAG += 1  # Increases difficulty for the next game if player plays again.

        if rounds == 1:
            print('\nWOW! You are Epic, you\'ve guessed my number in "first" round!')
        else:
            print(f"\nCongrats! you've guessed my number in {rounds} rounds, you've become a Mastermind.")

    # Player is out of lives:
    else:
        print(f"\nGame over! My secret number was {secret_number}.")


if __name__ == "__main__":
    print("Welcome to my Mastermind Game!")
    print("Let's make you Smarter at guessing.")
    time.sleep(1)
    mastermind()
    while play_again(FLAG):
        time.sleep(1)
        mastermind()
    time.sleep(1)
    print("Bye, Thanks for playing!")
