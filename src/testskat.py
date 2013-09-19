'''
Created on Sep 6, 2013

@author: paco
'''
import unittest
import skat
import itertools


class Test(unittest.TestCase):

    def setUp(self):
        self.big_table = skat.Table(["Seff", "Adam", "Cecily", "Brian",
                                     "Treffan", "Jed", "Julie"])
        self.short_table = skat.Table(['cpu', "Adam", 'cpu'])

    def testRanking(self):
        c1, c2, c3 = skat.Card("C", "K"), skat.Card("D", "J"), skat.Card("H",
                                                                         "T")
        cards = [c1, c2, c3]
        hand = skat.Hand()
        for card in cards:
            hand.add_card(card)
        self.assertNotEqual(hand.hand_rank(), 30)

#     def testLongGame(self):
#         while not self.big_table.finished:
#             self.big_table.play_round()

    def testShortGame(self):
        while not self.short_table.finished:
            self.big_table.play_round()

    def testPossibleHands(self):
        deck = skat.Deck()
        itertools.permutations()

if __name__ == "__main__":
    unittest.main()
