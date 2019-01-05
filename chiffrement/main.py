
from chiffrement import encryption_modes
from chiffrement.file_management import read_files_v2, write_file
from chiffrement.idea import idea_encryption, idea_decryption
import secrets
import os



def encrypt_file(file_name, new_file_name, mode_of_operation, enc_key, key_length):
    blocks = read_files_v2(file_name)
    blocks = mode_of_operation(blocks, enc_key, idea_encryption, key_length)
    write_file(new_file_name, blocks)


def decrypt_file(file_name, new_file_name, mode_of_operation, dec_key, key_length):
    blocks = read_files_v2(file_name)
    blocks = mode_of_operation(blocks, dec_key, idea_decryption, key_length)
    write_file(new_file_name, blocks)


def ask_users_var_chiffrement():
    """Permet d'obtenir les variables de chiffrement auprès de l'utilisateur."""
    cipher_mode = None
    key_length = None
    #choix mode chiffrement
    while True:
        choix = int(input("Veuillez choisir un mode de chiffrement :\n"
                      "1. ECB (déconseillé)\n" + "2. CBC\n" + "3. PCBC\n"))
        if choix == 1:
            cipher_mode = encryption_modes.ecb_encryption
            break
        elif choix == 2:
            cipher_mode = encryption_modes.cbc_encryption
            break
        elif choix == 3:
            cipher_mode = encryption_modes.pcbc_encryption
            break
    #choix taille de la clef
    while True:
        choix2 = int(input("Veuillez choisir les spécificités de la clef :\n"
                      "1. Utiliser une clef de 96 bits\n" + "2. Utiliser une clef de 128 bits\n" +
                      "3. Utiliser une clef de 160 bits\n" + "4. Utiliser une clef de 256 bits\n" +
                      "5. Utiliser une clef de la taille que vous désirez \n" +
                      "6. Rentrer une clef (en décimal) et l'utiliser\n"))
        if choix2 > 0 and choix2 < 6:
            if choix2 == 1:
                key_length = 96
            elif choix2 == 2:
                key_length = 128
            elif choix2 == 3:
                key_length = 160
            elif choix2 == 4:
                key_length = 256
            elif choix2 == 5:
                key_length = int(input("Veuillez rentrez la taille de la clef (en bits):\n"))
            clef_chiffrement = secrets.randbits(key_length)
            break
        elif choix2 == 6:
            clef_chiffrement = int(input("Veuillez rentrez votre clef en décimal :\n"))
            key_length = int(input("Veuillez rentrez la taille de votre clef (en bits):\n"))
            break
    #choix des fichiers
    while True:
        fichier_orig = input("Veuillez rentrer le chemin vers le fichier a chiffrer.\n")
        if os.path.isfile(fichier_orig):
            break
        else:
            print("Le chemin vers le fichier à chiffrer est incorrect.")
    while True:
        fichier_chif = input("Veuillez rentrer le chemin vers le fichier de sortie.\n")
        if os.path.isdir(os.path.dirname(fichier_chif)):
            break
        else:
            print("Le chemin vers le dossier de résultat est incorrect.")
    return fichier_orig, fichier_chif, cipher_mode, clef_chiffrement, key_length


def ask_user_dechiffrement():
    # choix mode déchiffrement
    while True:
        choix = int(input("Veuillez choisir un mode de déchiffrement (le même mode que pour le chiffrement):\n"
                          "1. ECB \n" + "2. CBC\n" + "3. PCBC\n"))
        if choix == 1:
            decipher_mode = encryption_modes.ecb_decryption
            break
        elif choix == 2:
            decipher_mode = encryption_modes.cbc_decryption
            break
        elif choix == 3:
            decipher_mode = encryption_modes.pcbc_decryption
            break

    # choix des fichiers
    while True:
        fichier_orig = input("Veuillez rentrer le chemin vers le fichier à déchiffrer.\n")
        if os.path.isfile(fichier_orig):
            break
        else:
            print("Le chemin vers le fichier à déchiffrer est incorrect.")
    while True:
        fichier_chif = input("Veuillez rentrer le chemin vers le fichier de sortie (une fois qu'il sera déchiffré).\n")
        if os.path.isdir(os.path.dirname(fichier_chif)):
            break
        else:
            print("Le chemin vers le dossier de résultat est incorrect.")
    return fichier_orig, fichier_chif, decipher_mode


def ask_user_chiffrement_sans_clef():
    # choix mode déchiffrement
    while True:
        choix = int(input("Veuillez choisir un mode de chiffrement :\n"
                          "1. ECB \n" + "2. CBC\n" + "3. PCBC\n"))
        if choix == 1:
            decipher_mode = encryption_modes.ecb_encryption
            break
        elif choix == 2:
            decipher_mode = encryption_modes.cbc_encryption
            break
        elif choix == 3:
            decipher_mode = encryption_modes.pcbc_encryption
            break

    # choix des fichiers
    while True:
        fichier_orig = input("Veuillez rentrer le chemin vers le fichier à chiffrer.\n")
        if os.path.isfile(fichier_orig):
            break
        else:
            print("Le chemin vers le fichier à chiffrer est incorrect.")
    while True:
        fichier_chif = input("Veuillez rentrer le chemin vers le fichier de sortie (une fois qu'il sera chiffré).\n")
        if os.path.isdir(os.path.dirname(fichier_chif)):
            break
        else:
            print("Le chemin vers le dossier de résultat est incorrect.")
    return fichier_orig, fichier_chif, decipher_mode


if __name__ == '__main__':
    pass
    # clef = random.randrange(0, 2**64-1)
    # encrypt_file(r'D:\Users\Crowbar\PycharmProjects\GS15\w a t.jpg',
    #              r'D:\Users\Crowbar\PycharmProjects\GS15\w a t_chiffré.txt',
    #              cfb_encryption, enc_key=clef, key_length=64)
    # decrypt_file(r'D:\Users\Crowbar\PycharmProjects\GS15\w a t_chiffré.txt',
    #              r'D:\Users\Crowbar\PycharmProjects\GS15\w a t déchiffré.jpg',
    #              cfb_decryption, dec_key=clef, key_length=64)
    # print(ask_users_var())
