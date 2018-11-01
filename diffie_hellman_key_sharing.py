import miller_rabin_test as mrt
from Crypto.Util import number

def main():
    print("""PARTAGE DE CLEF : DIFFIE HELLMAN""")
    p, j = prime_number_choice()
    g = pair_generator(p, j)
    alice_key, a = alice_key_generator(g, p)
    bob_key, b = bob_key_generator(g, p)
    shared_key = shared_key_generator(bob_key, a, p)

"""1. Alice choisit un entier premier (grand), noté p ;"""
def prime_number_choice():
    print("""Choix du nombre premier de l'espace générateur.\n\n
    Quel est son choix ?\n
    ->1<- Générer automatiquement un premier de 1024 bits.\n
    ->2<- Entrer manuellement un premier (non conseillé pour la suite).
    """)
    while 1:
        choix = input("Choississez une option.\n")
        if choix == '1':
            q_length = 256
            p_length = 1024
            q = number.getPrime(q_length)
            j = number.getRandomInteger(p_length-q_length)
            while (j % 2 != 0):
                j = number.getRandomInteger(p_length - q_length)
            while not (mrt.is_Prime(j*q + 1)):
                j = number.getRandomInteger(p_length - q_length)
                while (j % 2 != 0):
                    j = number.getRandomInteger(p_length - q_length)
            p = j * q + 1
            print("Le nombre généré est " + str(p))
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
    return p, j

"""2. Alice cherche un générateur alpha du corps Zp ;"""
def pair_generator(p, j):
    h = number.getRandomInteger(1023)
    while ((h^j)%p == 1):
        h = number.getRandomInteger(1023)
    g = (h^j)%p
    print("Le générateur est " + str(g))
    return g

"""3. Alice choisit un entier a 2 Zp et calcule A = a ; ce résultat A est envoyé à Bob"""
def alice_key_generator(g, p):
    print("C'est au tour d'Alice.\n\n")
    a_size = 255
    a = number.getRandomInteger(a_size)
    alice_key = (g^b)%p
    print("Sa clef secrète est : " + str(alice_key))
    return  alice_key, a

"""4. Bob choisit un entier b 2 Zp et calcule B = B ; ce résultat B est envoyé à Alice"""
def bob_key_generator(g, p):
    print("C'est au tour de Bob.\n\n")
    b_size = 255
    b = number.getRandomInteger(b_size)
    bob_key = (g^b)%p
    print("Sa clef secrète est : " + str(bob_key))
    return  bob_key, b

def shared_key_generator(bob_key, a, p):
    shared_key = (bob_key^a)%p
    print("La clef partagée entre Alice et Bob telle que définie par l'algorithme de Diffie Hellman est : \n" + str(shared_key))
    return shared_key

if __name__ == "__main__":
    main()