

from chiffrement.file_management import read_files_v2, write_file
from chiffrement.idea import idea_encryption, idea_decryption



def encrypt_file(file_name, new_file_name, mode_of_operation, enc_key, key_length):
    blocks = read_files_v2(file_name)
    blocks = mode_of_operation(blocks, enc_key, idea_encryption, key_length)
    write_file(new_file_name, blocks)


def decrypt_file(file_name, new_file_name, mode_of_operation, dec_key, key_length):
    blocks = read_files_v2(file_name)
    blocks = mode_of_operation(blocks, dec_key, idea_decryption, key_length)
    write_file(new_file_name, blocks)


# if __name__ == '__main__':
#     clef = random.randrange(0, 2**64-1)
#     encrypt_file(r'D:\Users\Crowbar\PycharmProjects\GS15\w a t.jpg',
#                  r'D:\Users\Crowbar\PycharmProjects\GS15\w a t_chiffré.txt',
#                  cfb_encryption, enc_key=clef, key_length=64)
#     decrypt_file(r'D:\Users\Crowbar\PycharmProjects\GS15\w a t_chiffré.txt',
#                  r'D:\Users\Crowbar\PycharmProjects\GS15\w a t déchiffré.jpg',
#                  cfb_decryption, dec_key=clef, key_length=64)





# if __name__ == '__main__':
#     print("""Quelles opérations souhaitez vous faire ?\n
#     ->1<- Générer une clé publique / privée.\n
#     ->2<- Authentifier une clé publique / un certificat.\n
#     ->3<- Partager une clé secrète.\n
#     ->4<- Utiliser une clé secrète pour chiffrer un message (et le signer).\n
#     ->5<- Déchiffrer un message et vérifier la signature.\n
#     ->6<- Complet, salade, tomate oignon.""")
#     while 1:
#         choix = input("Choississez une option.")
#         if choix == 1:
#             pass
#         elif choix == 2:
#             pass
#         elif choix == 3:
#             pass
#         elif choix == 4:
#             pass
#         elif choix == 5:
#             pass
#         elif choix == 6:
#             pass
#         else:
#             print("Entrez un chiffre entre 1 et 6 svp.")

