import random
from Crypto.Util import number
from sympy import mod_inverse
import main_pack.hashing_sha3


#LES CLEFS AURONT CETTE STRUCTURES POUR RSA !

def key_gen(key_size):
    """ Return : clef_publique, clef_privee : (n, e), (p, q, d)"""
    p = number.getPrime(key_size)
    q = number.getPrime(key_size)
    n = p * q
    phin = (p-1)*(q-1)
    while True:
        e = random.randrange(1, phin)
        if number.GCD(e,phin) == 1:
            break
    d = mod_inverse(e, phin)
    return (n, e), (p, q, d)


def rsa_cipher(msg, n, exposant):
    return pow(msg, exposant, n)


def verifier_clef(clef_signe, signature, c_publique):
    """Utilise la clef publique de l'authorité pour vérifier la signature."""
    # empreinte = ''
    # for i in clef_signe:
    #     empreinte += str(i)
    # # empreinte = hash(empreinte) # UTILISER LA FONCTION DE HASH DE MARTIN
    empreinte = key_to_hash(clef_signe)
    if rsa_cipher(signature, c_publique[0], c_publique[1]) == empreinte:
        return True
    else:
        return False


def signer_clef(clef_a_signer, clef_privee):
    """ Signe une clef publique. Comme dans l'énoncé, la clef a signer est en 3 partie (A, alfa, p)"""
    # empreinte = ''
    # for i in clef_a_signer:
    #     empreinte += str(i)
    # empreinte = hash(empreinte) # UTILISER LA FONCTION DE HASH DE MARTIN
    empreinte = key_to_hash(clef_a_signer)
    return rsa_cipher(empreinte, clef_privee[0]*clef_privee[1], clef_privee[2])


def key_to_hash(clef_publique_a_signe):
    empreinte = ''
    for i in clef_publique_a_signe:
        empreinte += str(i)
    return int(main_pack.hashing_sha3.hash_document(format(int(empreinte), 'b')), 2)


def verifier_hash(empreinte, signature, c_publique):
    if rsa_cipher(signature, c_publique[0], c_publique[1]) == empreinte:
        return True
    else:
        return False


def signer_hash(empreinte, clef_privee):
    return rsa_cipher(empreinte, clef_privee[0] * clef_privee[1], clef_privee[2])


if __name__ == '__main__':
    pass
    # clef_signer = (66545456, 6156, 11348949556)
    # clef_signer = (random.randrange(2 ** 512 - 1), random.randrange(2 ** 512 - 1), random.randrange(2 ** 512 - 1))
    # clef_publique, clef_privee = key_gen(1024)
    # signature = signer_clef(clef_signer, clef_privee)
    # print(verifier_clef(clef_signer, signature, clef_publique))

    # cipher_m = rsa_cipher(clear, clef_privee[0]*clef_privee[1], clef_privee[2])
    # decipher = rsa_cipher(cipher_m, clef_publique[0], clef_publique[1])
    # print(clear)
    # print(cipher_m)
    # print(decipher)
    # print(verifier(clear, cipher_m, clef_publique))
