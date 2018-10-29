import numpy as np
import sys
import toolbox as tb
from Lib.LFSR import lfsr as lfsr

""
"Cette fonction prend en entrée un fichier codé en binaire et renvoie en sortie le hash du fichier"
""


def main():
    """

    :return:
    """
    hash_length, size_c, size_block, size_r, n_ite = initialisation()
    doc = tb.load_input()
    docbin = str(tb.str_to_bin(doc))
    doc_w_padding = str(tb.padding(size_r, docbin))
    hash_hex, hash_bin = hashage(doc_w_padding, n_ite, size_c, size_r, hash_length)
    print(hash_hex)


def initialisation():
    """

    :return:
    """
    # Initialisation des variables en fonction de l'énoncé et du choix utilisateur.
    # hashLength = selectHashLenght()

    # TEMP
    hash_length = 384

    size_c = 2 * hash_length
    size_block = 1600
    n_ite = 24
    size_r = size_block - size_c
    return hash_length, size_c, size_block, size_r, n_ite


def select_hash_lenght():
    """

    :return:
    """
    print("""Quelles taille de Hash voulez vous ?\n
    ->1<- 256 bits.\n
    ->2<- 384 bits.\n
    ->3<- 512 bits.\n""")
    choix = False
    while not choix:
        choix = input("Choisissez une option.")
        if choix == '1':
            return 256
        elif choix == '2':
            return 384
        elif choix == '3':
            return 512
        else:
            print("Entrez un chiffre entre 1 et 3 svp.")


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
    les sous bloc ri et ci sont  constitués des premiers et des derniers bits du bloc Bi.
    """
    for n in range(0, n_ite):
        r = string_hashing[:size_r]
        string_p = doc_w_padding[n * size_r:-(n + 1) * size_r]
        r_xor = tb.xor_bin(r, string_p)
        string_hashing = r_xor + string_hashing[-size_c:]
        block_hashing = string_to_array(string_hashing)

        block_hashing, string_hashing = hashing_function(block_hashing)
        """
        6. les sous bloc ri et ci sont respectivement constitués des premiers et des derniers bits du bloc Bi.
        """

    """
    PHASE DE RECUPERATION
    """
    m = hash_length / size_r

    r = string_hashing[:size_r]
    block_hashing_init, string_hashing = hashing_function(block_hashing)

    hash_bin = str(string_hashing[:hash_length])
    print(hash_bin)
    # for n in range(1, m):
    #    r_hash = string_hashing[:size_r]
    #   block_hashing_init, string_hashing = hashing_function(block_hashing_init)
    #    hash = hash + r_hash

    # print(len(hash))
    hash_hex = hex(int(hash_bin, 2))
    return hash_hex, hash_bin


def hashing_function(block_hashing_init):
    """

    :param block_hashing_init:
    :return:
    """
    global k
    block_hashing_etape1 = block_hashing_init

    """
    1. on remplace chaque bit de chaque sous-blocs de 64 bits par un XOR avec le bit de parité d’une colone
    adjacente : B[:; j; k]   B[:; j; k]  parite(B[:; j; k 􀀀 1]) ;
    """
    for j in range(0, 5):
        for k in range(0, 64):
            block_slice = str(tb.xor_bin(''.join(block_hashing_init[:, j, k]),
                                         tb.parity_bit(''.join(block_hashing_init[:, j, k - 1]))))
            block_hashing_etape1[:, j, k] = list(str(block_slice))

        block_slice = tb.xor_bin(''.join(block_hashing_init[:, j, 0]),
                                 tb.parity_bit(''.join(block_hashing_init[:, j, 63])))
        block_hashing_etape1[:, j, 0] = list(block_slice)
    """
    2. on permute les blocs de 64 bits de t bits avec t qui dépend de la position dans le tableaux (vous pourrez
    définir t en fonction des indices (i; j) comme vous le souahitez ; B[i; j; :]   B[i; j; :] << t(i; j) ;
    """
    f_i = 3
    f_j = 2
    block_hashing_etape2 = block_hashing_etape1
    for i in range(0, 5):
        for j in range(0, 5):
            block_hashing_etape2[i, j, :] = block_hashing_etape1[tb.addition_mod(f_i, i, 5),
                                            tb.addition_mod(j, f_j, 5),
                                            :]

    """
    3. on permute les sous-blocs de 64 bits du tableau : B[i; j; :]   B[j; 2i+3j; :] (attention à la permutation
    des lignes et des colones) avec ici, bien sûr, 2i + 3jmod5 ;
    """
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
                                     tb.logical_and(''.join(block_hashing_etape3[i, j + 1, :]),
                                                    ''.join(block_hashing_etape3[i, j - 1, :])))
            block_hashing_etape4[i, j, :] = list(block_slice)

    """
    5. on effectue une dernière opération de XOR entre certains bits des mots de 64 bits : B[j; j; :]  
    B[j; j; 2m 􀀀 1]  B[j; j;m + 7  L(m)] avec m = f0; : : : ; 6g, 20 􀀀 1 = 􀀀1  63mod64 et L(m)
    correspondant à la sortie (un bit) d’un LFSR de 8 bits.
    """
    block_hashing_etape5 = block_hashing_etape4
    # for j in range (0, 4):
    #    block_slice = tb.xor_bin(block_hashing_etape4[j,j,2^m_LFSR(L)])

    block_hashing_init = block_hashing_etape5
    string_hashing = array_to_string(block_hashing_etape5)
    print(string_hashing)
    return block_hashing_init, string_hashing


def array_to_string(block_hashing):
    """

    :param block_hashing:
    :return:
    """
    string_hashing = ''.join(block_hashing[0, 0, :])
    for i in range(1, 5):
        for j in range(1, 5):
            string_hashing = string_hashing + ''.join(block_hashing[i, j, :])

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
