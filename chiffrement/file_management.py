def read_files_v2(file_name):
    """Retourne un array de int sur 64 bits constitué des données du fichier"""
    blocks = []
    with open(file_name, mode='rb') as f:
        data = f.read()
        if len(data) % 8 != 0:
            for i in range(8 - len(data) % 8):
                data = b"".join([data, b"\x00"])
        for i in range(0, len(data), 8):
            blocks.append(int.from_bytes(data[i:i+8], byteorder='big', signed=False))
    return blocks


def write_file(file_name, data):
    """
    Ecrit le tableau d'entier donné en entrée en bytes dans le fichier spécifié par file_name.
    :param file_name:
    :param data: list of 64 bit unsigned integer
    :return:
    """
    bin_data = []
    for a in data:
        bin_data.append(int(a).to_bytes(8, byteorder='big', signed=False))
    bin_data = b"".join(bin_data)
    with open(file_name, mode='wb') as f:
        f.write(bin_data)


def read_in_bin(filename):
    """Extrait le contenu binaire d'un fichier, et le retourne sous la forme d'une str de 0 et de 1."""
    bin_str = ""
    with open(filename, mode='rb') as f:
        data = f.read()
    for a in data:
        bin_str += format(a, 'b')
    return bin_str


if __name__ == '__main__':
    data = read_in_bin(r'D:\Users\Crowbar\PycharmProjects\GS15\test.txt')
    print(data)