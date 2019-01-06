import random
from collections import deque
import sympy


def idea_encryption(enc_key, bloc, key_length = 128):
    """ Un wrapper pouvant être utilisé par les méthodes du fichier encryption_modes.py"""
    return idea(True, enc_key, bloc, key_length)


def idea_decryption(enc_key, bloc, key_length = 128):
    """ Un wrapper pouvant être utilisé par les méthodes du fichier encryption_modes.py"""
    return idea(False, enc_key, bloc, key_length)


def idea(encryption, enc_key, bloc, key_length):
    """
    La fonction de chiffrement / déchiffrement d'IDEA.
    :param encryption: Si TRUE : les sous clefs de chiffrement sont utilisé, sinon ce sont les clefs de déchiffrement.
    :param enc_key: La clef de chiffrement.
    :param bloc: Le bloc à chiffrer (int)
    :param key_length: La longueur de la clef, en bit (pour la génération des sous clefs)
    :return: le bloc chiffré / déchiffré (int)
    """
    if encryption is True:
        subkeys = subkey_creation(key=enc_key, key_length=key_length)
    else:
        # subkeys = get_dec_subkeys(enc_key, key_length)
        subkeys = get_dec_subkeys_V2(enc_key, key_length)
    s_blocs = get_sub_blocs(bloc)
    for i in range(8):
        key_round = subkeys[i*6:i*6+6]   # the keys to use for this round
        s_blocs[0] = mmult(key_round[0], s_blocs[0])
        s_blocs[1] = (s_blocs[1] + key_round[1])%65536
        s_blocs[2] = (s_blocs[2] + key_round[2])%65536
        s_blocs[3] = mmult(key_round[3], s_blocs[3])
        t1 = s_blocs[0] ^ s_blocs[2]
        t2 = s_blocs[1] ^ s_blocs[3]
        t1 = mmult(t1, key_round[4])
        t2 = (t2 + t1) % 65536
        t2 = mmult(t2, key_round[5])
        t1 = (t1 + t2) % 65536
        s_blocs[0] = s_blocs[0] ^ t2
        s_blocs[2] = s_blocs[2] ^ t2
        s_blocs[1] = s_blocs[1] ^ t1
        s_blocs[3] = s_blocs[3] ^ t1
        s_blocs[1], s_blocs[2] = s_blocs[2], s_blocs[1]
    s_blocs[1], s_blocs[2] = s_blocs[2], s_blocs[1]
    s_blocs[0] = mmult(subkeys[48], s_blocs[0])
    s_blocs[1] = (s_blocs[1] + subkeys[49]) % 65536
    s_blocs[2] = (s_blocs[2] + subkeys[50]) % 65536
    s_blocs[3] = mmult(subkeys[51], s_blocs[3])
    return get_whole_bloc(s_blocs)


def get_dec_subkeys_V2(enc_key, key_length):
    """Une fonction produisant les sous clef de déchiffrement à partir de la clef de chiffrement. Elle fait appel à
    subkey_creation pour travailler à partir des sous clefs de chiffrement."""
    enc_subkeys = subkey_creation(key=enc_key, key_length=key_length)
    dec_subkeys = [None] * 52
    for i in range(6, 43, 6):
        dec_subkeys[i] = mod_inverse(enc_subkeys[48-i], 65537)
        dec_subkeys[i+1] = mod_opp(enc_subkeys[50-i], 65536)
        dec_subkeys[i+2] = mod_opp(enc_subkeys[49-i], 65536)
        dec_subkeys[i+3] = mod_inverse(enc_subkeys[51-i], 65537)
        dec_subkeys[i+4] = enc_subkeys[46-i]
        dec_subkeys[i+5] = enc_subkeys[47-i]
    #1ère ligne
    dec_subkeys[0] = mod_inverse(enc_subkeys[48], 65537)
    dec_subkeys[1] = mod_opp(enc_subkeys[49], 65536)
    dec_subkeys[2] = mod_opp(enc_subkeys[50], 65536)
    dec_subkeys[3] = mod_inverse(enc_subkeys[51], 65537)
    dec_subkeys[4] = enc_subkeys[46]
    dec_subkeys[5] = enc_subkeys[47]
    #dernière ligne
    dec_subkeys[48] = mod_inverse(enc_subkeys[0], 65537)
    dec_subkeys[49] = mod_opp(enc_subkeys[1], 65536)
    dec_subkeys[50] = mod_opp(enc_subkeys[2], 65536)
    dec_subkeys[51] = mod_inverse(enc_subkeys[3], 65537)
    return dec_subkeys


def mod_inverse(a, m):
    """Un wrapper autour de la fonction mod_inverse de sympy"""
    if a != 0:
        inv = sympy.mod_inverse(a,m)
    else:
        inv = 65536
    if mmult(a,inv) != 1:
        raise ValueError("L'inverse trouvé ne colle pas !!!")
    return inv


def mod_opp(a, m):
    """Une fonction permettant de récuperer et de vérifier la validité de l'opposé modulaire."""
    if a > m :
        raise Exception("Problème dans la valeur de a !")
    opp = m - a
    if ((a + opp) % m) != 0:
        raise Exception("L'opposé n'annule pas !")
    return opp


def mmult(a, b):
    """La multiplication comme défini dans IDEA."""
    mod = 65537
    if a == 0:
        a = 65536
    if b == 0:
        b = 65536
    c = (a * b) % mod
    if c == 65536:
        return 0
    else:
        return c


def subkey_creation(key: int, key_length: int):
    """Fonction permettant de créer les sous clefs grâce à la clef de chiffrement (un int positif)."""
    if key < 0:
        raise Exception("Key is a negative number, must be positive.")
    key = format(key, 'b')
    key = "0"*(key_length-len(key)) + key
    intermediate_subkeys = [key[i:i+16] for i in range(0, len(key), 16)]
    all_subkeys = []
    while len(all_subkeys) < 52:
        for ind, sub_k in enumerate(intermediate_subkeys):
            intermediate_subkeys[ind] = permutation_circulaire(sub_k)
            all_subkeys.append(sub_k)
    all_subkeys = all_subkeys[:52]
    for i in range(len(all_subkeys)):
        all_subkeys[i] = int(all_subkeys[i], 2)
    return all_subkeys


def get_sub_blocs(bloc):
    """Divise le bloc (int) en 4 sous blocs (int)."""
    s_blocs = int(bloc).to_bytes(8, byteorder='big', signed=False)
    s_blocs = [int.from_bytes(s_blocs[i:i + 2], byteorder='big', signed=False) for i in range(0, 8, 2)]
    return s_blocs


def get_whole_bloc(s_blocs):
    """Reconstruit les 4 sous blocs de la fin d'IDEA en un bloc"""
    bloc_fin = ""
    for a in s_blocs:
        bin = format(a, 'b')
        bin = '0'*(16-len(bin)) + bin
        bloc_fin += bin
    return int(bloc_fin, 2)


def permutation_circulaire(a: str):
    """Un fonction permettant d'effectuer une permutation circulaire."""
    a = deque(a)
    a.rotate(-25)
    return "".join(a)


if __name__ == '__main__':
    pass
    # key_l = 256
    # clef = random.randrange(2 ** key_l)
    # bloc = random.randrange(2 ** 64)
    # cypher_bloc = idea(True, clef, bloc, key_length=key_l)
    # clear_bloc = idea(False, clef, cypher_bloc, key_length=key_l)
    # print(bloc)
    # print(clear_bloc)

