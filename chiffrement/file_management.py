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

    :param file_name:
    :param data: list of 64 bit unsigned integer
    :return:
    """
    bin_data = []
    for a in data:
        bin_data.append(int(a).to_bytes(8, byteorder='big', signed=False))      #comment signaler que des bytes ont été rajouté aux blocs
    bin_data = b"".join(bin_data)
    with open(file_name, mode='wb') as f:
        f.write(bin_data)




if __name__ == '__main__':
    blocks = read_files_v2('test.dat')
    write_file('reecrit.dat', blocks)