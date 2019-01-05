import numpy as np
import sys
import toolbox as tb
import math
from Lib.LFSR import lfsr as lfsr

""
"Cette fonction prend en entrée un fichier codé en binaire et renvoie en sortie le hash du fichier"
""


def main():
    """

    :return:
    """

    print("""HASHAGE : SHA3""")
    hash_length, size_c, size_block, size_r = initialisation()
    doc = tb.load_input()
    docbin = str(tb.str_to_bin(doc))
    doc_w_padding = str(tb.padding(size_r, docbin))
    n_ite = int(len(doc_w_padding)/size_r)
    #print("Il y aura " + str(n_ite) + " itérations.")
    hash_hex, hash_bin = hashage(doc_w_padding, n_ite, size_c, size_r, hash_length)
    print("Le hash SHA3 du fichier est : ")
    print(hash_hex)


def hash_document(doc_bin):
    """

    :param doc_bin:
    :return:
    """
    hash_length, size_c, size_block, size_r = initialisation()
    doc_w_padding = str(tb.padding(size_r, doc_bin))
    n_ite = int(len(doc_w_padding) / size_r)
    # print("Il y aura " + str(n_ite) + " itérations.")
    hash_hex, hash_bin = hashage(doc_w_padding, n_ite, size_c, size_r, hash_length)
    print("Le hash SHA3 du fichier est : ")
    print(hash_hex)
    return hash_hex


def initialisation():
    """
    :return: hash_length, size_c, size_block, size_r
    """
    #PAR DEFAUT : hash_length = 384 bits
    hash_length = 384
    while True:
        print("""CALCUL DU HASH DU FICHIER\n
        Quelles taille de hash voulez vous ?\n
        ->1<- 256 bits\n
        ->2<- 384 bits\n
        ->3<- 512 bits\n """)
        choix = int(input("Choississez une option."))

        if choix == 1:
            hash_length = 256
            break

        elif choix == 2:
            break

        elif choix == 3:
            hash_length = 512
            break
        else:
            print("Mauvais choix : on utilise 384 bits par défaut")
            break

    size_c = 2 * hash_length
    size_block = 1600
    size_r = size_block - size_c
    return hash_length, size_c, size_block, size_r


def hashage(doc_w_padding, n_ite, size_c, size_r, hash_length):
    """
    :param hash_length:
    :param doc_w_padding:
    :param n_ite:
    :param size_c:
    :param size_r:
    :return:
    """
    """
    Création premier bloc = que des 0
    Initialisation du LFSR
    """
    block_hashing_zeroes = [[["0" for k in range(64)] for j in range(5)] for i in range(5)]
    block_hashing_init = np.asarray(block_hashing_zeroes)
    string_hashing = array_to_string(block_hashing_init)

    state = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    L = lfsr.LFSR(fpoly=[8, 4, 3, 2], initstate=state)  # Prime function of degree 8 : x^8 + x^4 + x^3 + x^2 + 1

    """
    PHASE D'ABSOPTION
    le nombre d’itération est fixé à n = 24 ;
    c = 2p.
    les sous bloc ri et ci sont constitués des premiers et des derniers bits du bloc Bi.
    """
    for n in range(0, n_ite):
        # print("itération n°" + str(n + 1))
        r = string_hashing[:size_r]
        # print("r = " + str(r))
        string_p = doc_w_padding[n * size_r:(n + 1) * size_r]

        # print("string p = " + str(string_p))
        r_xor = tb.xor_bin(r, string_p)
        string_hashing = r_xor + string_hashing[:size_c]
        # print("string_hashing = " + str(len(string_hashing)))
        block_hashing = string_to_array(string_hashing)
        # print("block_hashing taille = " + str(len(array_to_string(block_hashing))))
        for m in range(0, 23):
            block_hashing, string_hashing, L = hashing_function(block_hashing, L)
        """
        6. les sous bloc ri et ci sont respectivement constitués des premiers et des derniers bits du bloc Bi.
        """

    """
    PHASE DE RECUPERATION
    """
    m = int(math.ceil(hash_length / size_r))
    print("hash lenght = " + str(hash_length) + " et size_r = " + str(size_r))
    print("m = " + str(m))
    r = string_hashing[size_r:]
    block_hashing, string_hashing, L = hashing_function(block_hashing, L)
    # hash_bin = str(string_hashing[:hash_length])
    # print(hash_bin)
    r_hash = string_hashing[:hash_length]
    block_hashing, string_hashing, L = hashing_function(block_hashing, L)
    print(r_hash)
    hash = r_hash
    """
    for x in range(1, m):
        r_hash = string_hashing[size_r:]
        print(r_hash)
        block_hashing, string_hashing, L = hashing_function(block_hashing, L)
        hash = hash + r_hash
    # print(len(hash))
    """
    hash_hex = hex(int(hash, 2))
    print(len(hash))
    return hash_hex, hash


def hashing_function(block_hashing_init, L):
    """

    :param block_hashing_init:
    :return:
    """
    global k
    block_hashing_etape1 = block_hashing_init
    # print("à l'étape 0 : " + str(array_to_string(block_hashing_etape1)))

    """
    1. on remplace chaque bit de chaque sous-blocs de 64 bits par un XOR avec le bit de parité d’une colone
    adjacente : B[:; j; k]   B[:; j; k]  parite(B[:; j; k 􀀀 1]) ;
    """
    for j in range(0, 5):
        for k in range(1, 64):
            block_slice = str(tb.xor_bin(''.join(block_hashing_init[:, j, k]),
                                         tb.parity_bit(''.join(block_hashing_init[:, j, k - 1]))))
            block_hashing_etape1[:, j, k] = list(str(block_slice))

        block_slice = tb.xor_bin(''.join(block_hashing_init[:, j, 0]),
                                 tb.parity_bit(''.join(block_hashing_init[:, j, 63])))
        block_hashing_etape1[:, j, 0] = list(block_slice)

    #print("à l'étape 1 : " + str(array_to_string(block_hashing_etape1)))

    """
    2. on permute les blocs de 64 bits de t bits avec t qui dépend de la position dans le tableaux (vous pourrez
    définir t en fonction des indices (i; j) comme vous le souahitez ; B[i; j; :]   B[i; j; :] << t(i; j) ;
    """
    """
    f_i = 3
    f_j = 2
    block_hashing_etape2 = block_hashing_etape1
    for i in range(0, 5):
        for j in range(0, 5):
            block_hashing_etape2[i, j, :] = block_hashing_etape1[tb.addition_mod(f_i, i, 5),
                                            tb.addition_mod(j, f_j, 5),
                                            :]
    print("à l'étape 2 : " + str(array_to_string(block_hashing_etape2)))
"""
    """
    3. on permute les sous-blocs de 64 bits du tableau : B[i; j; :]   B[j; 2i+3j; :] (attention à la permutation
    des lignes et des colones) avec ici, bien sûr, 2i + 3jmod5 ;
    """
    block_hashing_etape2 = block_hashing_etape1
    block_hashing_etape3 = block_hashing_etape2
    for i in range(0, 5):
        for j in range(0, 5):
            block_hashing_etape3[i, j, :] = block_hashing_etape2[j, tb.addition_mod(2 * i, 3 * j, 5), :]

    """
    4. on effectue un XOR entre les lignes : B[:; j; :]   B[:; j; :]  (B[:; j + 1; :]&B[:; j - 1; :]) ;
    """
    block_hashing_etape4 = block_hashing_etape3
    for j in range(0, 4):
        for i in range(0, 5):
            block_slice = tb.xor_bin(''.join(block_hashing_etape3[i, j, :]),
                                     tb.logical_and(''.join(block_hashing_etape3[i, (j + 1)%5, :]),
                                                    ''.join(block_hashing_etape3[i, j - 1, :])))
            block_hashing_etape4[i, j, :] = list(block_slice)
    block_slice = tb.xor_bin(''.join(block_hashing_etape3[i, j, :]),
                             tb.logical_and(''.join(block_hashing_etape3[i, 1, :]),
                                            ''.join(block_hashing_etape3[i, 4, :])))
    block_hashing_etape4[i, j, :] = list(block_slice)
    """
    5. on effectue une dernière opération de XOR entre certains bits des mots de 64 bits : B[j; j; :]  
    B[j; j; 2m 􀀀 1]  B[j; j;m + 7  L(m)] avec m = f0; : : : ; 6g, 20 􀀀 1 = 􀀀1  63mod64 et L(m)
    correspondant à la sortie (un bit) d’un LFSR de 8 bits.
    """
    block_hashing_etape5 = block_hashing_etape4
    for m in range(0, 7):
        for j in range(1, 5):
            block_hashing_etape5[j, j, m] = tb.xor_bin(block_hashing_etape4[j,j,(2^m-1)%64], block_hashing_etape4[j,j,(m+7*L.next())%64])

    block_hashing_fin = block_hashing_etape5
    string_hashing = array_to_string(block_hashing_etape5)
    print(string_hashing)
    return block_hashing_fin, string_hashing, L


def array_to_string(block_hashing):
    """

    :param block_hashing:
    :return:
    """
    string_hashing = '0'
    for i in range(0, 5):
        for j in range(0, 5):
            string_hashing = string_hashing + ''.join(block_hashing[i, j, :])

    string_hashing = string_hashing[1:]
    # print(len(string_hashing))
    return string_hashing


def string_to_array(string_hashing):
    """

    :param string_hashing:
    :return:
    """
    block_hashing_tab = [[["0" for y in range(64)] for x in range(5)] for z in range(5)]
    block_hashing = np.asarray(block_hashing_tab)
    n = 0
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, 64):
                block_hashing[i, j, k] = string_hashing[n]
                n = n + 1

    # print(len(block_hashing))
    return block_hashing


def m_LFSR(L):
    """

    :param L:
    :return:
    """
    m = str(L.next())
    for i in range(1, 8):
        m = m + str(L.next())
    return int(m, 2)


if __name__ == "__main__":
    main()
