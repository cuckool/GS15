import random


def ecb_encryption(plain_text, enc_key, encryption_function, key_length):
    """
    Une entrée de la liste plain_text >> un bloc de 64 bits
    """
    cypher_txt = []
    for i in plain_text:
        cypher_txt.append(encryption_function(enc_key, i, key_length))
    return cypher_txt


def ecb_decryption(cypher_txt, dec_key, decryption_function, key_length):
    plain_text = []
    for i in cypher_txt:
        plain_text.append(decryption_function(dec_key, i, key_length))
    return plain_text


def cbc_encryption(plain_text, enc_key, encryption_function, key_length):
    """
    Retourne une list avec un nb de plus en [0], le bloc qui ne pourra pas être décodé sans l'IV
    Une entrée de la liste plain_text >> un bloc de 64 bits
    """
    cypher_txt = []
    plain_text_cp = plain_text[:]
    plain_text_cp.insert(0, random.randrange(0, 2**64-1))
    initialisation_vector = random.randrange(0, 2**64-1)
    for i in plain_text_cp:
        temp = initialisation_vector ^ i
        cypher_bloc = encryption_function(enc_key, temp, key_length)
        initialisation_vector = cypher_bloc
        cypher_txt.append(cypher_bloc)
    return cypher_txt


def cbc_decryption(cypher_txt, dec_key, decryption_function, key_length):
    plain_text = []
    for ind, i in enumerate(cypher_txt[1:]):
        temp = decryption_function(dec_key, i, key_length)
        res = temp ^ cypher_txt[ind]                #ça devrait être ind-1 mais, enumerate est sur cypher_txt[1:], donc le index de cet enumerate est le ind-1 de enumerate(cypher)
        plain_text.append(res)
    return plain_text


def pcbc_encryption(plain_text, enc_key, encryption_function, key_length):
    """
    Une entrée de la liste plain_text >> un bloc de 64 bits
    """
    cypher_txt = []
    initialisation_vector = enc_key #Comment déduire l'IV de la clé sans pouvoir la retrouver depuis lui ?? Hash de 64 bits ??
    for index, block in enumerate(plain_text):
        temp = initialisation_vector ^ block
        cypher_bloc = encryption_function(enc_key, temp, key_length)
        cypher_txt.append(cypher_bloc)
        initialisation_vector = block ^ cypher_bloc
    return cypher_txt


def pcbc_decryption(cypher_txt, dec_key, decryption_function, key_length):
    """
        Une entrée de la liste plain_text >> un bloc de 64 bits
    """
    plain_text = []
    initialisation_vector = dec_key
    for ind, block in enumerate(cypher_txt):
        temp = decryption_function(dec_key, block, key_length)
        plain_block = initialisation_vector ^ temp
        plain_text.append(plain_block)
        initialisation_vector = block ^ plain_block
    return plain_text


def cfb_encryption(plain_text, enc_key, encryption_function, key_length):
    """
    Retourne une list avec un nb de plus en [0], le bloc qui ne pourra pas être décodé sans l'IV
    Une entrée de la liste plain_text >> un bloc de 64 bits
    """

    raise Exception("Cette fonction n'est pas opérationnelle pour l'écriture sur fichier.")

    cypher_txt = []
    plain_text_cp = plain_text[:]
    plain_text_cp.insert(0, random.randrange(0, 2**64-1))
    initialisation_vector = random.randrange(0, 2**64-1)
    for block in plain_text_cp:
        temp = encryption_function(enc_key, initialisation_vector, key_length)
        cypher_block = block ^ temp
        initialisation_vector = cypher_block
        cypher_txt.append(cypher_block)
    return cypher_txt


def cfb_decryption(cypher_txt, dec_key, encryption_function, key_length):

    raise Exception("Cette fonction n'est pas opérationnelle pour l'écriture sur fichier.")

    plain_text = []
    for ind, i in enumerate(cypher_txt[1:]):
        temp = encryption_function(dec_key, cypher_txt[ind], key_length) #ça devrait être ind-1 mais, enumerate est sur cypher_txt[1:], donc le index de cet enumerate est le ind-1 de enumerate(cypher)
        res = temp ^ i
        plain_text.append(res)
    return plain_text


def test_function(key, plaintext, key_length):
    """
    Doit respecter la forme:
     entrée : int sur 64 bits (max 2**64-1) + key de 64 bits
     retourne : le bloc chiffré
    """
    return key ^ plaintext


