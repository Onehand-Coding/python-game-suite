import random
import shelve

import pygame

from .config import DATA_DIR

pygame.init()


class Lucky9:
    def __init__(self, player):
        self.dealers = {
            5: {"Robin": 1_000_000},
            4: {"Caesar": 800_000},
            3: {"Jeric": 600_000},
            2: {"Joko": 400_000},
            1: {"Ace": 200_000},
        }
        self.level = 1
        self.player = player
        self.deck = self.createDeck()
        self.dealer = self.inviteDealer()
        self.dataFolder = DATA_DIR
        if not self.dataFolder.exists():
            self.dataFolder.mkdir()
        self.database = self.dataFolder / "lucky_data"

    @staticmethod
    def createDeck():
        suits = [
            chr(9830),  # Diamonds
            chr(9829),  # Hearts
            chr(9824),  # Spades
            chr(9827),  # Clubs
        ]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        cards = [(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(cards)
        return cards

    def inviteDealer(self):
        dealer = self.dealers.get(self.level)
        dealerName = list(dealer.keys())[0]
        dealerMoney = dealer.get(dealerName)
        return Dealer(dealerName, dealerMoney)

    def getPlayerNames(self):
        with shelve.open(self.database) as db:
            return list(db.keys())

    def saveData(self, name=""):
        if not name:
            name = self.player.name
        with shelve.open(self.database, writeback=True) as db:
            db[name] = {
                "level": self.level,
                "money": self.player.money,
                "debt": self.player.debt,
                "dealer name": self.dealer.name,
                "dealer money": self.dealer.money,
                "times refused to pay": self.player.timesRefusedToPay,
            }

    def loadGameData(self, name):
        with shelve.open(self.database) as db:
            self.level = db[name]["level"]
            self.player.debt = db[name]["debt"]
            self.player.money = db[name]["money"]
            self.player.timesRefusedToPay = db[name]["times refused to pay"]
            dealerName = db[name]["dealer name"]
            dealerMoney = db[name]["dealer money"]
            self.dealer = Dealer(dealerName, dealerMoney)

    def deletePlayerData(self, name):
        with shelve.open(self.database) as db:
            del db[name]

    def clearData(self):
        for file in self.dataFolder.iterdir():
            file.unlink()


class Player:
    def __init__(self, name: str, money=10_000):
        self.name = name
        self.money = money
        self._debt = 0
        self.hand = []
        self.bet = None
        self.timesRefusedToPay = 0

    def __str__(self):
        return f"\nPangalan: {self.name} \nPera: {self.money:,} Pesos \nUtang: {self.debt:,} Pesos"

    @property
    def debt(self):
        return self._debt

    @debt.setter
    def debt(self, value):
        self._debt = value

    def showHand(self, revealHand=True):
        lines = ["", "", "", ""]
        for i, card in enumerate(self.hand):
            if not revealHand:
                lines[0] += " ___ "
                lines[1] += "|#  |"
                lines[2] += "| ##|"
                lines[3] += "|__#|"
            else:
                rank, suit = card
                lines[0] += " ___ "
                lines[1] += "|{} |".format(rank.ljust(2))
                lines[2] += "| {} |".format(suit)
                lines[3] += "|_{}|".format(rank.rjust(2, "_"))
        for i in lines:
            print(i)

    def getHandValue(self, revealHandValue=True):
        value = 0
        aces = []
        ranks = []

        if not revealHandValue:
            return "??"

        for card in self.hand:
            rank, suit = card
            ranks.append(rank)
            if rank == "A":
                value += 1
                aces.append(card)
            else:
                value += int(rank)

        value %= 10

        cardCounts = len(self.hand)
        if (cardCounts == 3 and len(set(ranks)) == 1) or (
            cardCounts == 2 and len(aces) == 2
        ):
            value = 9

        return value


class Dealer(Player):
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []

    def __str__(self):
        return f"{self.name}\nPera: {self.money:,} Pesos"
