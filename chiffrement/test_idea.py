import unittest
import random
import idea


class TestIDEA(unittest.TestCase):

    def test_encryption_decryption(self):
        for i in range(1000):
            clef = random.randrange(2 ** 128)
            bloc = random.randrange(2 ** 64)
            self.assertEqual(bloc, idea.idea_decryption(clef, idea.idea_encryption(clef, bloc)))
