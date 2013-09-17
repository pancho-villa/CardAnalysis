'''
Created on Sep 6, 2013

@author: paco
'''
import unittest
import skat


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTable(self):
        #======================================================================
        # table = skat.Table(['Seff', "Adam", 'weasel'])
        #======================================================================
        table = skat.Table(["Seff", "Adam", "Cecily", "Brian", "Treffan",
                             "Jed", "Julie"])
        while not table.finished:
            table.play_round()

if __name__ == "__main__":
    unittest.main()
