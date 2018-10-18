import numpy as np
import sys

""
"Cette fonction prend en entrée un fichier codé en binaire et renvoie en sortie le hash du fichier"
""

def main():
    hashLength, c, sizeBlock, r, B = initialisation()
    doc = choixInput()
    padding(sizeBlock, doc)

def initialisation():
    # Initialisation des variables en fonction de l'énoncé et du choix utilisateur.
    #hashLength = selectHashLenght()


    #TEMP
    hashLength = 256


    print(hashLength)
    c = 2 * hashLength
    sizeBlock = 1600
    r = sizeBlock - c
    B = np.zeros((25, 25, 64))
    return hashLength, c, sizeBlock, r, B


def selectHashLenght():
    print("""Quelles taille de Hash voulez vous ?\n
    ->1<- 256 bits.\n
    ->2<- 384 bits.\n
    ->3<- 512 bits.\n""")
    choix = False
    while not choix:
        choix = input("Choisissez une option.")
        if choix == '1':
            choix = False
            return 256
        elif choix == '2':
            choix = False
            return 384
        elif choix == '3':
            choix = False
            return 512
        else:
            print("Entrez un chiffre entre 1 et 3 svp.")



def choixInput():
    doc = open("Bible.txt", "rb").read()
    print(doc)
    doc = 10011110000011111010101100001
    return doc

def padding(sizeBlock, doc):
    sizeDoc = sys.getsizeof(doc)
    print(sizeDoc)
    sizePadding = sizeDoc % sizeBlock
    print(sizePadding + sizeBlock)
    print(type(doc))
    print(format(int(doc), '0' + str(sizePadding + sizeDoc) + 'b'))
    doc = format(int(doc), '0' + str(sizePadding + sizeDoc) + 'b')
    print(sys.getsizeof(doc)%sizeBlock)



if __name__ == "__main__":
    main()