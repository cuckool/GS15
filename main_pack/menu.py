from chiffrement import main, encryption_modes, file_management
from certificat import rsa
import os
from main_pack import hashing_sha3, diffie_hellman_key_sharing




def generation_clef_pri_pu(clef_de_chiffrement_publique, clef_de_chiffrement_privee):
    """ Permet de générer les clefs publique et privée pour la signature."""
    if clef_de_chiffrement_privee != None and clef_de_chiffrement_publique != None:
        choix_changement = int(input("Il y a déjà des clefs de chiffrement publique/priveé. "
                                     "Voulez-vous en changer ?\n "
                                     "Vous ne pourrez plus authentifier les documents signés avec le précédent"
                                     " jeu de clef.\n"
                                     "1. Pour changer \n2. Pour garder les mêmes clefs."))
    else:
        choix_changement = 1
    if choix_changement == 1:
        pu_pri_key_length = int(
            input("Quelle taille (en bits) pour les clefs publique/privées pour la signature ? "
                  "Recommandation : supérieur a 1024."))
        return rsa.key_gen(pu_pri_key_length)
    elif choix_changement == 2:
        return clef_de_chiffrement_publique, clef_de_chiffrement_privee


def chiffrement_fichier(clef_chiffrement_idea, clef_chiffrement_idea_long):
    """La fonction permettant de chiffer un fichier en prenant en compte les choix de l'utilisateur."""
    if clef_chiffrement_idea is None:
        fichier_orig, fichier_chif, cipher_mode, clef_chiffrement_idea, clef_chiffrement_idea_long = main.ask_users_var_chiffrement()
    else:
        fichier_orig, fichier_chif, cipher_mode = main.ask_user_chiffrement_sans_clef()
    main.encrypt_file(fichier_orig, fichier_chif, cipher_mode, clef_chiffrement_idea,
                      clef_chiffrement_idea_long)

    bin_string = file_management.read_in_bin(fichier_orig)
    empreinte_fichier = int(hashing_sha3.hash_document(bin_string), 2)  #                                 générer clef chiffrement publique/privé > signé le doc#faut implémenter la signature : hash de martin > générer clef chiffrement publique/privé > signé le doc
    signature_fichier = rsa.signer_hash(empreinte=empreinte_fichier, clef_privee=clef_de_chiffrement_privee)
    with open(os.path.join(os.path.dirname(fichier_chif), 'signature_fichier.txt'), mode='w') as f:
        f.write(str(signature_fichier))
    print("Fichier chiffré avec succès :")
    print(fichier_chif)
    print("Signature :")
    print(os.path.join(os.path.dirname(fichier_chif), 'signature_fichier.txt'))
    return fichier_chif, cipher_mode, clef_chiffrement_idea, clef_chiffrement_idea_long


def dechiffrement_fichier(fichier_a_dechif, fichier_dechif, decipher_mode, option6=False):
    """La fonction permettant de déchiffer un fichier en prenant en compte les choix de l'utilisateur."""
    if not option6:
        fichier_a_dechif, fichier_dechif, decipher_mode = main.ask_user_dechiffrement()
    main.decrypt_file(fichier_a_dechif, fichier_dechif, decipher_mode, dec_key=clef_chiffrement_idea,
                      key_length=clef_chiffrement_idea_long)
    with open(os.path.join(os.path.dirname(fichier_a_dechif), 'signature_fichier.txt'), mode='r') as f_d:
        signature_fichier_dechiffre = int(f_d.read())



    #empreinte_fichier_dechif = 9815616816315616  # FAUT METTRE LE HASH DE MARTIN SUR LE FICHIER DECHIFF ICI
    bin_string2 = file_management.read_in_bin(fichier_dechif)
    empreinte_fichier_dechif = int(hashing_sha3.hash_document(bin_string2), 2)

    if rsa.verifier_hash(empreinte_fichier_dechif, signature_fichier_dechiffre, clef_de_chiffrement_publique):
        print("La signature est valide.")
    else:
        print("La signature est invalide !")


if __name__ == '__main__':
    """ La fonction principale du programme, présentant un menu à l'utilisateur."""
    clef_chiffrement_idea = None
    clef_chiffrement_idea_long = None           # longueur de la clef IDEA
    clef_de_chiffrement_publique = None
    clef_de_chiffrement_privee = None


    while True:
        print("""Quelles opérations souhaitez vous faire ?\n
        ->1<- Générer une clé publique / privée.\n
        ->2<- Authentifier une clé publique / un certificat.\n
        ->3<- Partager une clé secrète.\n
        ->4<- Utiliser une clé secrète pour chiffrer un message (et le signer).\n
        ->5<- Déchiffrer un message et vérifier la signature.\n
        ->6<- Complet, salade, tomate oignon.""")
        choix = int(input("Choississez une option."))

        if choix == 1:
            clef_de_chiffrement_publique, clef_de_chiffrement_privee = generation_clef_pri_pu(
                clef_de_chiffrement_publique, clef_de_chiffrement_privee)

        elif choix == 2:
            if clef_de_chiffrement_privee == None or clef_de_chiffrement_publique == None:
                print(
                    "Il n'y a pas de clef de chiffrement privée/publique pour la signature. Elles vont être générées.")
                pu_pri_key_length = int(
                    input("Quelle taille (en bits) pour ces clefs ? Recommandation : supérieur a 1024."))
                clef_de_chiffrement_publique, clef_de_chiffrement_privee = rsa.key_gen(pu_pri_key_length)
            a, alfa, p = diffie_hellman_key_sharing.generer_clef_publique()
            signature_clef = int(rsa.signer_clef((a, alfa, p), clef_de_chiffrement_privee))
            print("Clef :", (a, alfa, p))
            print('Signature :', signature_clef)
            print("La signature est vérifiée :",rsa.verifier_clef((a, alfa, p), signature_clef, clef_de_chiffrement_publique))

        elif choix == 3:
            clef_chiffrement_idea, clef_chiffrement_idea_long = diffie_hellman_key_sharing.generer_clef_secrete()
            print("Clef générée grâce à Diffie-Hellman.")

        elif choix == 4:
            if clef_de_chiffrement_privee == None or clef_de_chiffrement_publique == None:
                print(
                    "Il n'y a pas de clef de chiffrement privée/publique pour la signature. Elles vont être générées.")
                pu_pri_key_length = int(
                    input("Quelle taille (en bits) pour ces clefs ? Recommandation : supérieur a 1024."))
                clef_de_chiffrement_publique, clef_de_chiffrement_privee = rsa.key_gen(pu_pri_key_length)

            bob, bab, clef_chiffrement_idea, clef_chiffrement_idea_long = chiffrement_fichier(clef_chiffrement_idea,
                                                                                              clef_chiffrement_idea_long)

        elif choix == 5:
            dechiffrement_fichier(None, None, None, option6=False)

        elif choix == 6:
            print("Génération de clef publique/privée pour la signature")
            clef_de_chiffrement_publique, clef_de_chiffrement_privee = generation_clef_pri_pu(
                clef_de_chiffrement_publique, clef_de_chiffrement_privee)
            # =================================================================================================
            clef_chiffrement_idea, clef_chiffrement_idea_long = diffie_hellman_key_sharing.generer_clef_secrete()
            print("Clef générée grâce à Diffie-Hellman.")
            # =================================================================================================
            fichier_chiffre, cipher_mode, clef_chiffrement_idea, clef_chiffrement_idea_long = chiffrement_fichier(
                clef_chiffrement_idea, clef_chiffrement_idea_long)
            # ==================================================================================================
            if cipher_mode == encryption_modes.ecb_encryption:
                decipher_mode = encryption_modes.ecb_decryption
            elif cipher_mode == encryption_modes.cbc_encryption:
                decipher_mode = encryption_modes.cbc_decryption
            elif cipher_mode == encryption_modes.pcbc_encryption:
                decipher_mode = encryption_modes.pcbc_decryption
            while True:
                fichier_sortie = input("Veuillez rentrer le chemin pour le fichier de sortie "
                                       "(une fois qu'il sera déchiffré).\n")
                if os.path.isdir(os.path.dirname(fichier_sortie)):
                    break
                else:
                    print("Le chemin vers le dossier de résultat est incorrect.")

            dechiffrement_fichier(fichier_chiffre, fichier_sortie, decipher_mode, option6=True)
