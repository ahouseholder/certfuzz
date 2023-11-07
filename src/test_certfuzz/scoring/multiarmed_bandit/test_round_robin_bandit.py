'''
Created on Feb 22, 2013

@organization: cert.org
'''
import unittest
from certfuzz.scoring.multiarmed_bandit.round_robin_bandit import RoundRobinMultiArmedBandit


class Test(unittest.TestCase):

    def setUp(self):
        self.mab = RoundRobinMultiArmedBandit()
        self.keys = 'abcdefghijklmnopqrstuvwxyz'
        for arm in self.keys:
            self.mab.add_item(arm, arm)

    def tearDown(self):
        pass

    def test_next(self):
        arms = 'abcdefghijklmnopqrstuvwxyz'
        for arm in arms:
            self.mab.add_item(arm, arm)

        i = 1
        n = 1000
        limit = n * len(arms)
        from collections import defaultdict
        seen = defaultdict(int)
        for arm in self.mab:
            if i > limit:
                break
            seen[arm] += 1
            i += 1

        for arm in arms:
            # ensure we saw each arm n times
            self.assertEqual(n, seen[arm])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
