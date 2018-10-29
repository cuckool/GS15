import binascii
import operator
import math

def str_to_bin(doc):
    docbin = ''.join(format(ord(x), 'b') for x in doc)
    return docbin

def load_input() :
    doc = open("Bible.txt", "r", encoding="ISO-8859-1").read()
    return doc

def left_shift(a):
    """
    :param a: binary in a string
    :return: binary in a string
    """
    x,a = a[0], a[1:]
    return a + x

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

def xor_bin(a, b):
    """
    :param a: String
    :param b: String
    :param len : int
    :return: String
    """
    xor_bin = '{0:b}'.format(int(a,2) ^ int(b,2))
    xor_bin = padding(len(a), xor_bin)
    return xor_bin

def addition_mod_216(a, b):
    return int(math.fmod(a + b, 65536)) #65536 = 2^16 (pour éviter de recalculer à chaque fois)

def multiplication_mod_216(a, b):
    return int(math.fmod(a*b, 65536))

def addition_mod(a, b, mod):
    return (a + b)% mod

def parity_bit(bin):
    a = int(str(bin), 2)
    if a%2 == 0:
        return "0"
    else: return "1"

def logical_and(bin1, bin2):
    return '{0:b}'.format(int(bin1, 2) & int(bin2 ,2))

def padding(size_r, doc):
    """

    :param size_r:
    :param doc:
    :return:
    """
    if (len(doc) != size_r):
        doc_padding = ("0" * (size_r - (len(doc)) % size_r)) + doc
    else : doc_padding = doc

    return doc_padding




