import unittest
import random
import encryption_modes


key_length_test = 128


class TestEncryptionModes(unittest.TestCase):
    def test_ecb(self):
        for a in range(1000):
            plain = [random.randrange(0, 2**key_length_test-1) for i in range(10)]
            enc_key = random.randrange(0, 2**key_length_test-1)
            cypher_text = encryption_modes.ecb_encryption(plain_text=plain, enc_key=enc_key,
                                                          encryption_function=encryption_modes.test_function, key_length = key_length_test)
            deciphered_txt = encryption_modes.ecb_decryption(cypher_txt=cypher_text, dec_key=enc_key,
                                                             decryption_function=encryption_modes.test_function, key_length = key_length_test)
            self.assertEqual(plain, deciphered_txt, msg="ECB : Le cypher et le plain text ne sont pas égaux.")

    def test_cbc(self):
        for a in range(1000):
            plain = [random.randrange(0, 2 ** key_length_test - 1) for i in range(10)]
            enc_key = random.randrange(0, 2 ** key_length_test - 1)
            cypher_text = encryption_modes.cbc_encryption(plain_text=plain, enc_key=enc_key,
                                                          encryption_function=encryption_modes.test_function, key_length = key_length_test)
            deciphered_txt = encryption_modes.cbc_decryption(cypher_txt=cypher_text, dec_key=enc_key,
                                                             decryption_function=encryption_modes.test_function, key_length = key_length_test)
            self.assertEqual(plain, deciphered_txt, msg="CBC : Le cypher et le plain text ne sont pas égaux.")

    def test_pcbc(self):
        for a in range(1000):
            plain = [random.randrange(0, 2 ** key_length_test - 1) for i in range(10)]
            enc_key = random.randrange(0, 2 ** key_length_test - 1)
            cypher_text = encryption_modes.pcbc_encryption(plain_text=plain, enc_key=enc_key,
                                                           encryption_function=encryption_modes.test_function, key_length = key_length_test)
            deciphered_txt = encryption_modes.pcbc_decryption(cypher_txt=cypher_text, dec_key=enc_key,
                                                             decryption_function=encryption_modes.test_function, key_length = key_length_test)
            self.assertEqual(plain, deciphered_txt, msg="PCBC : Le cypher et le plain text ne sont pas égaux.")

    # def test_cfb(self):
    #     for a in range(1000):
    #         plain = [random.randrange(0, 2 ** key_length_test - 1) for i in range(10)]
    #         enc_key = random.randrange(0, 2 ** key_length_test - 1)
    #         cypher_text = encryption_modes.cfb_encryption(plain_text=plain, enc_key=enc_key,
    #                                                        encryption_function=encryption_modes.test_function, key_length = key_length_test)
    #         deciphered_txt = encryption_modes.cfb_decryption(cypher_txt=cypher_text, dec_key=enc_key,
    #                                                          encryption_function=encryption_modes.test_function, key_length = key_length_test)
    #         self.assertEqual(plain, deciphered_txt, msg="CFB : Le cypher et le plain text ne sont pas égaux.")


if __name__ == '__main__':
    unittest.main(verbosity=2)