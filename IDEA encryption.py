import toolbox
import secrets
import math
"""
Manipulation des chaines en int, on repasse en binaires pour les XOR puis on les rends en int
"""
def chiffrer(message, key):
    print(key)
    print(message)
    #splitting key into 16 bit keys
    key_list = [key[x:x+16] for x in range(0, len(key), 16)]
    print(key_list)
    #creating the 52 subkeys
    subkey_list = []
    while len(subkey_list) < 52:                #gaffe que le nb de clef dans key_list soit un diviseur de 52 sinon possible problème au déchiffrement >>> en fait pas sur
        for i, key in enumerate(key_list):
            subkey_list.append(key[:])
            key_list[i] = toolbox.left_shift(key)
    print("subkey list",subkey_list)
    print(len(subkey_list))
    #splitting message into 4 blocks of 16 bits
    msg_blocs = [message[x:x + 16] for x in range(0, len(message), 16)]
    print("msg blocks",msg_blocs)
    for a in range(0, 7):
        subkey_set = subkey_list[a: a+6]
        msg_blocs[0] = toolbox.multiplication_mod_216(msg_blocs[0], subkey_set[1])



def generate_key(size):
    """
    :param size: int, number of bits of the key
    :return: key (binary)
    """
    a = bin(secrets.randbelow(int(math.pow(2, size))))[2:]
    a = '0' * (size - len(a)) + a
    return a

message = "0000111011101000010001011000011000001110111010000100010110000110"
chiffrer(message=message,key = generate_key(32))