from chiffrement import main
from certificat import rsa
import os


if __name__ == '__main__':
    clef_chiffrement_idea = None
    clef_chiffrement_idea_long = None           #longueur de la clef IDEA
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
                    input("Quelle taille (en bits) pour ces clefs ? Recommandation : supérieur a 1024."))
                clef_de_chiffrement_publique, clef_de_chiffrement_privee = rsa.key_gen(pu_pri_key_length)

        elif choix == 2:
            pass

        elif choix == 3:
            #diffie hellman
            pass

        elif choix == 4:
            fichier_orig, fichier_chif, cipher_mode, clef_chiffrement_idea, clef_chiffrement_idea_long = main.ask_users_var_chiffrement()
            main.encrypt_file(fichier_orig, fichier_chif, cipher_mode, clef_chiffrement_idea, clef_chiffrement_idea_long)
            if clef_de_chiffrement_privee == None or clef_de_chiffrement_publique == None:
                print("Il n'y a pas de clef de chiffrement privée/publique pour la signature. Elles vont être générées.")
                pu_pri_key_length = int(input("Quelle taille (en bits) pour ces clefs ? Recommandation : supérieur a 1024."))
                clef_de_chiffrement_publique, clef_de_chiffrement_privee = rsa.key_gen(pu_pri_key_length)

            empreinte_fichier = 9815616816315616                                            #FAUT METTRE LE HASH DE MARTIN SUR LE FICHIER a chiffrer ICI                                     générer clef chiffrement publique/privé > signé le doc#faut implémenter la signature : hash de martin > générer clef chiffrement publique/privé > signé le doc

            signature_fichier = rsa.signer_hash(empreinte=empreinte_fichier, clef_privee=clef_de_chiffrement_privee)
            with open(os.path.join(os.path.dirname(fichier_chif), 'signature_fichier.txt'), mode='w') as f:
                f.write(str(signature_fichier))
            print("Fichier chiffré avec succès :")
            print(fichier_chif)
            print("Signature :")
            print(os.path.join(os.path.dirname(fichier_chif), 'signature_fichier.txt'))

        elif choix == 5:
            fichier_a_dechif, fichier_dechif, decipher_mode = main.ask_user_dechiffrement()
            main.decrypt_file(fichier_a_dechif, fichier_dechif, decipher_mode, dec_key=clef_chiffrement_idea,
                              key_length=clef_chiffrement_idea_long)
            with open(os.path.join(os.path.dirname(fichier_a_dechif), 'signature_fichier.txt'), mode='r') as f_d:
                signature_fichier_dechiffre = int(f_d.read())

            empreinte_fichier_dechif = 9815616816315616                                             #FAUT METTRE LE HASH DE MARTIN SUR LE FICHIER DECHIFF ICI

            if rsa.verifier_hash(empreinte_fichier_dechif, signature_fichier_dechiffre, clef_de_chiffrement_publique):
                print("La signature est valide.")
            else:
                print("La signature est invalide !")

        elif choix == 6:
            pass
        elif int(choix) > 6 and int(choix) < 1:
            print("Entrez un chiffre entre 1 et 6 svp.")
