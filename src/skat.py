'''
Created on Sep 6, 2013

@author: paco
'''
import random
from operator import itemgetter


def main():
    table = Table(["Seff", "Adam", "weasel", 'cpu'])

    while not table.finished():
        table.play_round()


class Table:

    def __init__(self, players):
        self.players = [Player(name, None, 3) for name in players]
        self.finished = False
        self.deck = None
        self.round = None
        self.knocked = False
        self.player_knocker = None
        self.dealer = -1
        self.init_round()

    def init_round(self):
        self.deck = Deck()
        self.round = 1
        self.knocked = False
        self.player_knocker = None
        self.deck.shuffle()
        self.deck.start_discard()
        self.dealer += 1
        for p in self.players:
            p.hand = Hand()
            for _ in range(3):
                p.hand.add_card(self.deck.deal_card())

    def reset_scores(self):
        for p in self.players:
            p.score = 0

    def score_round(self):
        scoring = {}
        for p in self.players:
            scoring[p.name] = scoring.get(p.name, p.hand.hand_rank())
        lowest_value = min(scoring.items(), key=itemgetter(1))[1]
        skat = 31
        losers = []
        if skat in scoring.values():
            for k, v in scoring.items():
                if v != skat:
                    losers.append([p for p in self.players if p.name == k][0])
        else:
            for k, v in scoring.items():
                if v == lowest_value:
                    for p in self.players:
                        if k == p.name:
                            p.lose_round()
                            print(
          "{} lost a dollar and has {} remaining".format(p.name,
                                                              p.dollars))
                            losers.append(p)
        print("*" * 79 + "\n\n")
        for player in losers:
            print("{} loses this round!!".format(player.name))
            if player.dollars == 0:
                print("{} is out of the game!!!".format(player.name))
                self.players.remove(player)

        print("*" * 79 + "\n\n")
        print([p.name for p in self.players])
        if len(self.players) == 1:
            print("Game over, there's only one player!")
            self.finished = True
        self.init_round()

    def get_active_player(self):
        self.active_player_index = divmod(self.round + self.dealer,
                                            len(self.players))[1]
        self.active_player = self.players[self.active_player_index]

    def play_round(self):
        while True:
            self.get_active_player()
            if self.player_knocker is not None:
                print("{} has knocked".format(self.player_knocker))
            print("It's {}'s turn".format(self.active_player.name))

            if self.active_player.name == self.player_knocker:
                self.score_round()
                break
            else:
                print("is the player the knocker? {}".format(
                              self.active_player.name == self.player_knocker))

            print("It's now round: {}".format(self.round))
            print(self.deck.show_discard_pile())
            print(self.active_player.name)
            print(self.active_player.hand)
            print(self.active_player.hand.hand_rank())
            print("_-" * 40)
            print("Press P to pickup or K to knock")
            action = input("What do you want to do now? ")
            if action.lower() == "p":
                print("You can pickup the discard or from the deck")
                print("Press D for discard pile or F for fresh card " + \
                      "from the deck")
                print("_-" * 40 + "\n")
                while True:
                    pile = input("Which card do you wish to pickup? ")
                    if pile[0].lower() == 'd':
                        self.active_player.hand.add_card(
                                                     self.deck.deal_discard())
                        break
                    elif pile[0].lower() == 'f':
                        self.active_player.hand.add_card(self.deck.deal_card())
                        break
                print("Now discard one of your bloody cards!")
                print(self.active_player.hand)
                print("\n")
                while True:
                    indx = input("Press 1, 2, 3, or 4 to drop your card ")
                    if indx.isdigit() and int(indx) <= 4 and int(indx) >= 0:
                        break
                    print("invalid entry, please try again")
                discard = self.active_player.hand.discard(int(indx) - 1)
                self.deck.add_to_discard(discard)

                print("{} is now holding {}".format(self.active_player.name,
                                                self.active_player.hand))
                print("With a score of {}".format(
                                          self.active_player.hand.hand_rank()))
                self.active_player.score = self.active_player.hand.hand_rank()
                if self.active_player.hand.hand_rank() == 31:
                    self.score_round()
                    break
                print(self.deck.show_discard_pile())

            elif action[0].lower() == "k":
                if self.knocked:
                    print("You can't knock bitch, it's already happened")
                    continue
                else:
                    self.player_knocker = self.active_player.name
                    self.knocked = True
            self.round += 1


class Player:

    def __init__(self, name, hand, dollars):
        self.name, self.hand, self.dollars = name, hand, dollars

    def __str__(self):
        return self.hand

    def lose_round(self):
        self.dollars -= 1

    def score(self, score):
        self.score = score

    def ai(self, strategy):
        self.ai = strategy

    def discard(self, hand):
        pass

    def knock(self):
        pass

    def show_hand(self):
        print(self.name, 'has', self.hand)


class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return', '.join(map(str, self.cards))

    def suited(self):
        suits = []
        for card in self.cards:
            suit = card.value()[1]
            if len(suits) == 0:
                suits.append(suit)
            elif suits[0] != suit:
                return False
        return True

    def same_cards(self):
        kinds = set()
        value = set()
        for card in self.cards:
            rank, suit, kind = card.value()
            value.add(rank)
            kinds.add(kind)
        if len(value) == 1 and len(kinds) == 3:
            return True
        return False

    def hand_rank(self):
        if self.suited():
            return sum([c.value()[0] for c in self.cards])
        elif self.same_cards():
            return 30
        else:
            score = {}
            for i, card in enumerate(self.cards):
                rank, suit, kind = card.value()
                if i == 0 or suit not in score.keys():
                    score[suit] = score.get(suit, rank)
                else:
                    score[suit] += rank
            return max(score.values())

    def add_card(self, card):
        self.cards.append(card)

    def take_top(self):
        return self.cards.pop(0)

    def discard(self, position):
        return self.cards.pop(position)


class Deck:

    def __init__(self):
        self.cards = [Card(s, r) for s in Card.SUIT for r in Card.RANKS]
        self.discard_pile = []

    def __str__(self):
        return', '.join(map(str, self.cards))

    def shuffle(self):
        random.shuffle(self.cards)

    def show_discard_pile(self):
        return', '.join(map(str, self.discard_pile))

    def deal_card(self):
        return self.cards.pop(0)

    def deal_discard(self):
        return self.discard_pile.pop()

    def add_card(self, card):
        self.cards.append(card)

    def start_discard(self):
        self.discard_pile.append(self.cards.pop(0))

    def add_to_discard(self, card):
        self.discard_pile.append(card)


class Card:
    SUIT = "HSDC"
    RANKS = "23456789TJQKA"

    def __init__(self, suit, rank):
        self.suit, self.rank = suit, rank

    def __str__(self):
        return "{}{}".format(self.rank, self.suit)

    def value(self):
        if self.rank.isdigit():
            return int(self.rank), self.suit, self.rank
        elif self.rank == "A":
            return 11, self.suit, self.rank
        else:
            return 10, self.suit, self.rank


if __name__ == '__main__':
    num_players = input("How many players will play? ")
    main()
