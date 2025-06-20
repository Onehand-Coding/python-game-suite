import pickle
import sys
from pathlib import Path

import pygame
from lucky_class.gui import *

pygame.init()

# Window setup
WIDTH = 600
HEIGHT = 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky9 Game")
FPS = 60
CLOCK = pygame.time.Clock()

# constants
DEALER_POS = (50, 230)
PLAYER_POS = (410, 230)
DECK_POS = (240, 140)
DELAY_DURATION = 2_000
DISPLAY_WINNER_DURATION = 3_000

# Fonts
TEXT_FONT = pygame.font.SysFont("comicsans", 25)
SMALL_TEXT_FONT = pygame.font.SysFont("calibri", 20)

# tracks the time to impliment delays.
lastActionTime = 0

# Game Objects
currentState = GameState.DEALING
deck = Deck()
player = Player("Kenneth", 10_000)
dealer = Dealer("Bangka", 1_000_000)
goodButton = Button("GOOD", (100, 20), (215, 250))
coins = [
    Coin("red", 1_000, (320, 65)),
    Coin("blue", 5_000, (380, 65)),
    Coin("yellow", 10_000, (440, 65)),
    Coin("green", 20_000, (500, 65)),
]

# sound
BG_SOUND.play(-1)

# Folder to save game data
luckyFolder = Path.home() / ".Lucky9 data"
if not luckyFolder.exists():
    luckyFolder.mkdir()


def displayWinner(pos):
    winner = checkWinner()
    winnerText = TEXT_FONT.render(f"{winner}", True, WHITE)
    WINDOW.blit(winnerText, pos)


def checkWinner():
    if dealer.getHandValue() > player.getHandValue():
        LOSE_SOUND.play()
        dealer.money += player.bet
        player.money -= player.bet
        result = "Panalo ang Bangka!"
    elif dealer.getHandValue() < player.getHandValue():
        WIN_SOUND.play()
        dealer.money -= player.bet
        player.money += player.bet
        result = "Panalo ka!"
    else:
        TIE_SOUND.play()
        result = "Tabla!"
    return result


def dealCards():
    global deck
    if len(deck.cards) <= 10:
        deck.cards = deck.createDeck()
    if not dealer.hand and not player.hand:
        for i in range(2):
            dealer.hand.append(deck.deal())
            player.hand.append(deck.deal())


def resetGame():
    global currentState, lastActionTime

    currentState = GameState.DEALING
    lastActionTime = 0
    dealer.hand.clear()
    player.hand.clear()
    dealer.isHandRevealed = False
    player.isHandRevealed = False
    player.bet = 0
    player.madeBet = False


def displayCoins():
    for coin in coins:
        coin.display(WINDOW)
        if coin.isPressed() and not player.isHandRevealed and len(player.hand) != 3:
            if int(coin.value) <= player.money:
                player.bet = int(coin.value)
                player.madeBet = True
                BET_SOUND.play()


def saveGame():
    gameState = {"player_money": player.money, "dealer_money": dealer.money}
    with open(luckyFolder / "lucky9_data.pkl", "wb") as file:
        pickle.dump(gameState, file)


def loadGame():
    try:
        with open(luckyFolder / "lucky9_data.pkl", "rb") as file:
            gameState = pickle.load(file)
            player.money = gameState["player_money"]
            dealer.money = gameState["dealer_money"]
    except FileNotFoundError:
        pass


def handleState():
    global currentState, lastActionTime

    if currentState == GameState.DEALING:
        displayCoins()
        dealCards()
        currentState = GameState.PLAYER_TURN

    elif currentState == GameState.PLAYER_TURN:
        if deck.isPressed() and player.isHandRevealed and not dealer.isHandRevealed:
            player.hits(deck.deal())
            HITS_SOUND.play()
        if player.isHandPressed() and player.madeBet:
            player.revealHand()
            REVEAL_SOUND.play()
            if len(player.hand) == 3 and player.isHandRevealed:
                currentState = GameState.DEALER_TURN
        elif (
            goodButton.isPressed(GREEN, DARK_GREEN)
            and player.isHandRevealed
            and not dealer.isHandRevealed
        ):
            GOOD_SOUND.play()
            currentState = GameState.DEALER_TURN
        lastActionTime = pygame.time.get_ticks()

    elif currentState == GameState.DEALER_TURN:
        if pygame.time.get_ticks() - lastActionTime >= DELAY_DURATION:
            if dealer.getHandValue() < 7:
                dealer.hits(deck.deal())
                HITS_SOUND.play()
                currentState = GameState.WAITING
            else:
                dealer.revealHand()
                REVEAL_SOUND.play()
                currentState = GameState.END_ROUND
            lastActionTime = pygame.time.get_ticks()

    elif currentState == GameState.WAITING:
        if pygame.time.get_ticks() - lastActionTime >= DELAY_DURATION:
            dealer.revealHand()
            REVEAL_SOUND.play()
            currentState = GameState.END_ROUND
            lastActionTime = pygame.time.get_ticks()

    elif currentState == GameState.END_ROUND:
        if pygame.time.get_ticks() - lastActionTime >= DISPLAY_WINNER_DURATION:
            displayWinner((50, 100))
            pygame.display.update()
            pygame.time.delay(DISPLAY_WINNER_DURATION)
            resetGame()

    if pygame.key.get_pressed()[pygame.K_s]:
        saveGame()


def displayIntro():
    intro_text = TEXT_FONT.render("Tara Lucky9 tayo!", True, WHITE)
    WINDOW.blit(intro_text, (150, 100))

    menu_text = TEXT_FONT.render("Pindutin ang Space para maglaro.", True, WHITE)
    WINDOW.blit(menu_text, (100, 200))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def renderGame():
    displayCoins()
    dealCards()

    #  Button
    goodButton.display(WINDOW)

    # Deck
    deck.displayDeck(WINDOW, DECK_POS)
    cardCountText = SMALL_TEXT_FONT.render(f"bilang: {len(deck.cards)}", True, WHITE)
    WINDOW.blit(cardCountText, (230, 140 + 75))

    # Dealer
    dealer.displayHand(WINDOW, DEALER_POS)
    dealerHandValue = "??" if not dealer.isHandRevealed else dealer.getHandValue()
    dealerHandValueText = TEXT_FONT.render(
        f"{dealer.name}: {dealerHandValue}", True, WHITE
    )
    WINDOW.blit(dealerHandValueText, (50, 180))
    dealerMoneyText = TEXT_FONT.render(f"Pera: {dealer.money:,} Pesos", True, WHITE)
    WINDOW.blit(dealerMoneyText, (50, 300))

    # Player
    player.displayHand(WINDOW, PLAYER_POS)
    playerHandValue = "??" if not player.isHandRevealed else player.getHandValue()
    playerHandValueText = TEXT_FONT.render(f"Ikaw: {playerHandValue}", True, WHITE)
    WINDOW.blit(playerHandValueText, (410, 180))
    playerMoneyText = TEXT_FONT.render(f"Pera: {player.money:,} Pesos", True, WHITE)
    WINDOW.blit(playerMoneyText, (350, 300))
    if player.bet != 0:
        playerBetText = TEXT_FONT.render(f"Taya: {player.bet:,} Pesos", True, WHITE)
    else:
        playerBetText = TEXT_FONT.render(f"Taya: {player.bet:,}", True, WHITE)
    WINDOW.blit(playerBetText, (50, 50))
    choiceBetText = TEXT_FONT.render("Pumili ng taya:", True, WHITE)
    WINDOW.blit(choiceBetText, (190, 2))

    handleState()


def main():
    loadGame()
    displayIntro()
    while True:  # Main game loop.
        WINDOW.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        renderGame()

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
