import random
import shelve
from pathlib import Path

from .lucky_player import Dealer


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
        self.dataFolder = Path("~/.Lucky9 data").expanduser()
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
