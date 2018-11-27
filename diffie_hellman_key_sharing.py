import miller_rabin_test as mrt
import math
from Crypto.Util import number
from random import randint

def main():
    print("""PARTAGE DE CLEF : DIFFIE HELLMAN""")
    # p, j = prime_number_choice()
    # g = pair_generator(p, j)
    p = prime_number_choice()
    g = pair_generator(p)
    alice_key, a = alice_key_generator(g, p)
    bob_key, b = bob_key_generator(g, p)
    shared_key = shared_key_generator(bob_key, a , p)

"""1. Alice choisit un entier premier (grand), noté p ;"""
def prime_number_choice():
    print("""Choix du nombre premier de l'espace générateur.\n\n
    Quel est son choix ?\n
    ->1<- Utilise un premier de 2048 bits avec 2 pour générateur (défini dans RFC 3526) et un clef de 540 bits.\n
    ->2<- Entrer manuellement un premier (non conseillé pour la suite).
    """)
    while 1:
        choix = input("Choississez une option.\n")
        if choix == '1':
            q_length = 256
            p_length = 2048
            # q = number.getPrime(q_length)
            # j = number.getRandomInteger(p_length-q_length)
            # if j % 2 != 0:
            #     j = j + 1
            # while not (mrt.is_Prime(j*q + 1)):
            #     j = number.getRandomInteger(p_length - q_length)
            #     if j % 2 != 0:
            #         j = j + 1
            # p = j * q + 1
            phex = "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
            phex = phex.replace(" ", "")
            p = int(phex, 16)
            print("Le nombre premier de 2048 bits est : " + str(p))
            key_length = 540
            break
        elif choix == '2':
            while 1:
                p = int(input("Choisissez un nombre entier. Entrez 0 pour revenir au menu précédent.\n"))
                if p == 0:
                    print("""->1<- Générer automatiquement un premier de 1024 bits.\n
->2<- Entrer manuellement un premier.""")
                    break
                if mrt.is_Prime(p):
                    print("Le nombre " + str(p) + " est bien entier selon le test de Miller Rabin.")
                    break
                else:
                    print("Le nombre " + str(p) + " n'est pas entier selon le test de Miller Rabin.")
        else: print("Veuillez entrer une option correcte.")
    #return p, j
    return p

"""2. Alice cherche un générateur alpha du corps Zp ;"""
def pair_generator(p) :#, j):
    # g_size = 1
    # h = number.getRandomInteger(g_size)
    # while ((h^j)%p == 1):
    #     h = number.getRandomInteger(g_size)
    # g = (h^j)%p
    g = 2
    print("Le générateur est " + str(g) + "\n")
    return g

"""3. Alice choisit un entier a 2 Zp et calcule A = a ; ce résultat A est envoyé à Bob"""
def alice_key_generator(g, p):
    print("\nC'est au tour d'Alice.\n")
    a_size = randint(540, 540)
    a = number.getRandomInteger(a_size)
    alice_key = (g^a)%p
    print("Sa clef secrète est : " + str(alice_key) + "\n")
    return  alice_key, a

"""4. Bob choisit un entier b 2 Zp et calcule B = B ; ce résultat B est envoyé à Alice"""
def bob_key_generator(g, p):
    print("\nC'est au tour de Bob.\n")
    b_size = randint(540, 540)
    b = number.getRandomInteger(b_size)
    bob_key = (g^b)%p
    print("Sa clef secrète est : " + str(bob_key) + "\n")
    return  bob_key, b

def shared_key_generator(bob_key, a, p):
    shared_key = (bob_key^a)%p
    print("\nLa clef partagée entre Alice et Bob telle que définie par l'algorithme de Diffie Hellman est : \n" + str(shared_key))
    return shared_key

if __name__ == "__main__":
    main()