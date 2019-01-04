import unittest
import random
from chiffrement.encryption_modes import *
from chiffrement.main import encrypt_file, decrypt_file
import os
import hashlib

class TestEncryptionDecryptionMode(unittest.TestCase):
    created_files = []

    @classmethod
    def setUpClass(cls):
        bin_data = [int(random.randrange(0, 65536)).to_bytes(2, byteorder='big', signed=False) for a in range(1000)]
        bin_data = b"".join(bin_data)
        with open('test_file.txt', mode='wb') as f:
            f.write(bin_data)
        cls.created_files.append('test_file.txt')

    @classmethod
    def tearDownClass(cls):
        for file in cls.created_files:
            os.remove(file)

    def test_enc_dec_all_modes(self):

        # to add a new cyphering mode, please add a dictionary
        modes = [
            {'mode': 'ECB',
             'filename': 'test_file_ecb.txt',
             'filename_deci': 'test_file_deciphered_ecb.txt',
             'enc_mode': ecb_encryption,
             'dec_mode': ecb_decryption},

            {'mode': 'CBC',
             'filename': 'test_file_cbc.txt',
             'filename_deci': 'test_file_deciphered_cbc.txt',
             'enc_mode': cbc_encryption,
             'dec_mode': cbc_decryption},

            {'mode': 'PCBC',
             'filename': 'test_file_pcbc.txt',
             'filename_deci': 'test_file_deciphered_pcbc.txt',
             'enc_mode': pcbc_encryption,
             'dec_mode': pcbc_decryption},

            # {'mode': 'CFB',
            #  'filename': 'test_file_cfb.txt',
            #  'filename_deci': 'test_file_deciphered_cfb.txt',
            #  'enc_mode': cfb_encryption,
            #  'dec_mode': cfb_decryption},
        ]

        key_length_test = 64
        clef = random.randrange(0, 2 ** key_length_test - 1)

        with open("test_file.txt", mode='rb') as f:
            data = f.read()
            original_hash = hashlib.sha224(data).hexdigest()

        for c_m in modes:
            self.created_files.append(c_m['filename'])
            self.created_files.append(c_m['filename_deci'])
            encrypt_file('test_file.txt', c_m['filename'], c_m['enc_mode'],
                         enc_key = clef, key_length = key_length_test)
            decrypt_file(c_m['filename'], c_m['filename_deci'], c_m['dec_mode'],
                         dec_key=clef, key_length=key_length_test)

            with open(c_m['filename_deci'], mode='rb') as f:
                data = f.read()
                deciphered_hash = hashlib.sha224(data).hexdigest()
            self.assertEqual(original_hash, deciphered_hash, msg="Testing on " + c_m['mode'])