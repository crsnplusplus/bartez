import pickle


def bartez_trie_save_to_file(trie, file):
    binary_file = open(file, mode='wb')
    my_pickled_mary = pickle.dump(trie, binary_file)
    binary_file.close()
    print(my_pickled_mary)


def bartez_trie_load_from_file(file):
    binary_file = open(file, mode='rb')
    data = bytearray(binary_file.read())
    trie = pickle.loads(data)
    binary_file.close()
    return trie
