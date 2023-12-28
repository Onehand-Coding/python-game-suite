
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
        if (cardCounts == 3 and len(set(ranks)) == 1) or (cardCounts == 2 and len(aces) == 2):
            value = 9

        return value


class Dealer(Player):
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []

    def __str__(self):
        return f"{self.name}\nPera: {self.money:,} Pesos"
