import toolbox
import secrets
import math
"""
Manipulation des chaines en int, on repasse en binaires pour les XOR puis on les rends en int
"""
def chiffrer(message, key):
    """

    :param message: 64 bits to encrypt : bin
    :param key: the encryption key : bin
    :return:
    """
    print("key \t\t:",key)
    print("message \t:", message)
    #splitting key into 16 bit keys
    key_list = [key[x:x+16] for x in range(0, len(key), 16)]
    #creating the 52 subkeys
    subkey_list = []
    while len(subkey_list) < 52:                #gaffe que le nb de clef dans key_list soit un diviseur de 52 sinon possible problème au déchiffrement >>> en fait pas sur
        for i, key in enumerate(key_list):
            subkey_list.append(key[:])
            key_list[i] = toolbox.left_shift(key)
    print("subkey list bin",subkey_list)
    subkey_list = [int(subkey, 2) for subkey in subkey_list]
    print("subkey list int", subkey_list)

    #splitting message into 4 blocks of 16 bits
    msg_blocs_temp = [message[x:x + 16] for x in range(0, len(message), 16)]

    #converting to message blocs to integer
    msg_blocs = [int(bloc, 2) for bloc in msg_blocs_temp]
    print("msg blocks",msg_blocs)
    for a in range(0, 7):
        subkey_set = subkey_list[a*6: a*6+6]
        msg_blocs[0] = toolbox.multiplication_mod_216(msg_blocs[0], subkey_set[0])  #1
        msg_blocs[1] = toolbox.addition_mod_216(msg_blocs[1], subkey_set[1])        #2
        msg_blocs[2] = toolbox.addition_mod_216(msg_blocs[2], subkey_set[2])        #3
        msg_blocs[3] = toolbox.multiplication_mod_216(msg_blocs[3], subkey_set[3])  #4
        t1 = toolbox.xor(msg_blocs[0], msg_blocs[2])                                #5
        t2 = toolbox.xor(msg_blocs[1], msg_blocs[3])                                #6
        t1 = toolbox.multiplication_mod_216(t1, subkey_set[4])                      #7
        t2 = toolbox.addition_mod_216(t1, t2)                                       #8
        t2 = toolbox.multiplication_mod_216(t2, subkey_set[5])                      #9
        t1 = toolbox.addition_mod_216(t1, t2)                                       #10
        msg_blocs[0] = toolbox.xor(msg_blocs[0], t2)                                #11
        msg_blocs[2] = toolbox.xor(msg_blocs[2], t2)                                #12
        msg_blocs[1] = toolbox.xor(msg_blocs[1], t1)                                #13
        msg_blocs[3] = toolbox.xor(msg_blocs[3], t1)                                #14
        msg_blocs[1], msg_blocs[2] = msg_blocs[2], msg_blocs[1]
    msg_blocs[0] = toolbox.multiplication_mod_216(msg_blocs[0], subkey_list[-4])
    msg_blocs[1] = toolbox.addition_mod_216(msg_blocs[1], subkey_list[-3])
    msg_blocs[2] = toolbox.addition_mod_216(msg_blocs[2], subkey_list[-2])
    msg_blocs[3] = toolbox.multiplication_mod_216(msg_blocs[3], subkey_list[-1])
    [print(a) for a in msg_blocs]
    return msg_blocs








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