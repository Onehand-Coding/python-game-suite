# import random
# from enum import Enum

# import pygame

# from .colors import *
# from .config import ASSETS_DIR, DATA_DIR, SOUND_ASSETS_DIR, IMAGE_ASSETS_DIR

# pygame.init()

# BG_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "bg_music.wav"))
# WIN_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "win.wav"))
# LOSE_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "lose.wav"))
# TIE_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "tie.wav"))
# BET_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "bet.wav"))
# REVEAL_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "reveal.wav"))
# HITS_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "hits.wav"))
# GOOD_SOUND = pygame.mixer.Sound(str(SOUND_ASSETS_DIR / "good.mp3"))


# class GameState(Enum):
#     DEALING = 1
#     PLAYER_TURN = 2
#     DEALER_TURN = 3
#     WAITING = 4
#     END_ROUND = 5


# class Card:
#     def __init__(self, name):
#         self.suit, self.rank = name
#         self.name = name
#         self.value = int(self.rank)
#         self.imageFile = f"{self.suit}-{self.rank}.png"
#         self.imagePath = ASSETS_DIR / "card_images"
#         self.face = pygame.image.load(self.imagePath / self.imageFile)
#         self.back = pygame.image.load(self.imagePath / "back.png")
#         self.showFace = False

#     def display(self, screen, pos):
#         if not self.showFace:
#             self.rect = self.back.get_rect(topleft=pos)
#             screen.blit(self.back, self.rect)
#         else:
#             self.rect = self.face.get_rect(topleft=pos)
#             screen.blit(self.face, self.rect)


# class Deck:
#     def __init__(self):
#         self.suits = ("diamonds", "hearts", "spades", "clubs")
#         self.ranks = list(str(num) for num in range(1, 11))
#         self.cards = self.createDeck()
#         self.isClicked = False

#     def createDeck(self):
#         deck = [Card((suit, rank)) for suit in self.suits for rank in self.ranks]
#         random.shuffle(deck)
#         return deck

#     def deal(self):
#         return self.cards.pop()

#     def displayDeck(self, screen, pos):
#         x, y = pos
#         for card in self.cards:
#             card.display(screen, pos)

#     def isPressed(self):
#         action = False
#         mousePos = pygame.mouse.get_pos()
#         if self.cards[0].rect.collidepoint(mousePos):
#             if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
#                 self.isClicked = True
#                 action = True
#             if pygame.mouse.get_pressed()[0] == 0:
#                 self.isClicked = False
#         return action


# class Player:
#     def __init__(self, name, money):
#         self.name = name
#         self.money = money
#         self.bet = 0
#         self.hand = []
#         self.xPosSpacer = 10
#         self.showHandFace = False
#         self.isHandRevealed = False
#         self.madeBet = False

#     def hits(self, card):
#         if len(self.hand) == 2:
#             self.hand.append(card)
#         self.isHandRevealed = False

#     def revealHand(self):
#         for card in self.hand:
#             card.showFace = True
#         self.isHandRevealed = True

#     def displayHand(self, screen, pos):
#         x, y = pos
#         for i, card in enumerate(self.hand):
#             card.display(screen, (x + (i * self.xPosSpacer), y))

#     def isHandPressed(self):
#         action = False
#         if self.hand:
#             topmostCard = self.hand[0]
#             mousePos = pygame.mouse.get_pos()
#             if topmostCard.rect.collidepoint(mousePos):
#                 if pygame.mouse.get_pressed()[0] == 1 and not self.showHandFace:
#                     self.showHandFace = True
#                     action = True
#                 if pygame.mouse.get_pressed()[0] == 0:
#                     self.showHandFace = False
#         return action

#     def getHandValue(self):
#         value = 0
#         for i, card in enumerate(self.hand):
#             value += int(card.rank)
#             if value % 10 == 0:
#                 value = 0
#             else:
#                 value %= 10
#         return value


# class Dealer(Player):
#     isHandPressed = None

#     def __init__(self, name, money):
#         self.name = name
#         self.money = money
#         self.hand = []
#         self.xPosSpacer = 10
#         self.showHandFace = False
#         self.isHandRevealed = False


# class Coin:
#     coinValueFont = pygame.font.Font("freesansbold.ttf", 15)

#     def __init__(self, name, value, pos):
#         self.name = name
#         self.value = value
#         self.pos = pos
#         self.imageFile = name + ".png"
#         self.imagePath = ASSETS_DIR / "coin_images"
#         self.image = pygame.image.load(self.imagePath / self.imageFile)
#         self.rect = self.image.get_rect(midleft=(pos))
#         self.valueTextYSpacer = 40
#         self.valueTextXSpacer = 8
#         self.isClicked = False

#     def display(self, screen):
#         x, y = self.pos
#         valueText = self.coinValueFont.render(f"{self.value:,}", True, WHITE)
#         screen.blit(valueText, (x + self.valueTextXSpacer, y + self.valueTextYSpacer))
#         screen.blit(self.image, self.rect)

#     def isPressed(self):
#         action = False
#         mousePos = pygame.mouse.get_pos()
#         if self.rect.collidepoint(mousePos):
#             if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
#                 self.isClicked = True
#                 action = True
#             if pygame.mouse.get_pressed()[0] == 0:
#                 self.isClicked = False
#         return action


# class Button:
#     buttonFont = pygame.font.Font("freesansbold.ttf", 25)

#     def __init__(self, text, size, pos, textColor=WHITE):
#         self.isClicked = False
#         self.topRect = pygame.Rect(pos, size)
#         self.topColor = BLUE
#         self.textSurf = self.buttonFont.render(text, True, textColor)
#         self.textRect = self.textSurf.get_rect(center=self.topRect.center)

#     def display(
#         self,
#         screen,
#     ):
#         pygame.draw.rect(screen, self.topColor, self.topRect, border_radius=8)
#         screen.blit(self.textSurf, self.textRect)

#     def isPressed(self, onColor=SILVER, offColor=BLUE):
#         action = False
#         mousePos = pygame.mouse.get_pos()
#         if self.topRect.collidepoint(mousePos):
#             self.topColor = onColor
#             if pygame.mouse.get_pressed()[0]:
#                 self.isClicked = True
#             else:
#                 if self.isClicked:
#                     action = True
#                     self.isClicked = False
#         else:
#             self.topColor = offColor
#         return action
