import binascii
import operator
import math

def str_to_bin(a, b):
    a = a.encode(encoding='utf-8', errors="strict")
    b = b.encode(encoding='utf-8', errors="strict")

    a = bin(int(a.hex()))[2:]
    b = bin(int(b.hex()))[2:]
    return a,b

def xor(a, b):
    """
    :param a: int
    :param b: int
    :return: int
    """
    a = bin(a)[2:]
    b = bin(b)[2:]
    a = '0' * (16 - len(a)) + a #padding de 0 pour avoir des nb sur 16 bits
    b = '0' * (16 - len(b)) + b
    result = [0]*16
    for ind, c  in enumerate(a):
        if (c == "1" and b[ind] == "0") or ( c == "0" and b[ind] == "1"):
            result[ind] = 1
    str1 = ''.join(str(e) for e in result)
    return int(str1, 2)

def addition_mod_216(a, b):
    return int(math.fmod(a + b, 65536)) #65536 = 2^16 (pour éviter de recalculer à chaque fois)

def multiplication_mod_216(a, b):
    return int(math.fmod(a*b, 65536))

