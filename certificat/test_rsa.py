import unittest
from certificat import rsa
import random


class TestRSA(unittest.TestCase):
    def test_signature_verification_clef(self):
        for a in range(1000):
            clef_a_signer = (random.randrange(2**512-1), random.randrange(2**512-1), random.randrange(2**512-1))
            print(clef_a_signer)
            clef_publique, clef_privee = rsa.key_gen(1024)
            signature = rsa.signer_clef(clef_a_signer, clef_privee)
            self.assertTrue(rsa.verifier_clef(clef_a_signer, signature, clef_publique),
                            msg='Iteration numéro :' + str(a))

    def test_signature_verification_hash(self):
        for a in range(10):
            empreinte = random.randrange(2**1024-1)
            clef_publique, clef_privee = rsa.key_gen(1024)
            signature = rsa.signer_hash(empreinte, clef_privee)
            self.assertTrue(rsa.verifier_hash(empreinte, signature, clef_publique))