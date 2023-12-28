import time
from words import getWord

HANGMAN = {
    "win": """
+_____
|     |
      |
      |   \\o/
      |    |
    __|__ / \\""",
    "lost": """
       _____+
      |     |
      |     O
      |    /|\\
      |    / \\
    __|__""",
}
flag = 4


def play():
    print("Hello, welcome! let's play Hangman")
    time.sleep(2)
    print("Be wise or else you'll be Hanged :)")
    time.sleep(1)
    print("Let's begin!")
    print()
    hangman()


def play_again():
    print("play again?")
    while True:
        play_again = input("Y/n: ").upper().strip()
        if play_again not in ["Y", "N"]:
            continue
        elif play_again == "Y":
            print("Ok, Let's go!")
            time.sleep(2)
            return True
        else:
            print("Bye, Thanks for playing!")
            return False


def hangman():
    global flag
    word = getWord(flag)
    word_letters = set(word)  # Get unique letters.
    used_letters = []
    lives = len(word_letters)

    while len(word_letters) and lives != 0:
        letters = [letter if letter in used_letters else "_" for letter in word]
        print("\nWord to guess:", " ".join(letters))
        print(f"Lives: {lives}")
        print("Used letters", " ".join(used_letters))

        guess = input("\nEnter your guess: ").upper()
        if not guess.isalpha():
            print("\nEnter a letter!")
            continue
        elif len(guess) != 1:
            print("\nHey! use a single letter")
            continue
        elif guess in word_letters:
            if len(word_letters) != 1:
                print("\nNice! you've guessed a letter")
            used_letters.append(guess)
            word_letters.remove(guess)
        elif guess in used_letters:
            print(f"\nOops! letter {guess} already used")
        else:
            print(f"\nNope! letter {guess} not in word")
            used_letters.append(guess)
            lives -= 1
    print('-------------------')
    if len(word_letters) == 0:
        flag += 1
        print("Well played!")
        print("You've guessed the word \"" + word + '"')
        time.sleep(1)
        print(HANGMAN.get("win"))
    else:
        print("\nSorry about that :( ")
        time.sleep(1)
        print(HANGMAN.get("lost"))
        print(f"The word was: {word}")
    print()


play()

while play_again():
    hangman()
