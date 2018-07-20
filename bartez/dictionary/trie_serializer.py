import pickle

from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_pattern import BartezDictionaryTriePatternMatcher

def serialize_pattern_matcher(file_imported, language, matcher_file):
    trie_imported = bartez_trie_import_from_file(file_imported, language)
    matcher = BartezDictionaryTriePatternMatcher()
    matcher.set_language(language)
    matcher.load_from_dictionary_trie(trie_imported)

    binary_file = open(matcher_file, mode='wb')
    my_pickled_mary = pickle.dump(matcher, binary_file)
    print(my_pickled_mary)
    binary_file.close()


def deserialize_pattern_matcher(file):
    binary_file = open(file, mode='rb')
    data = bytearray(binary_file.read())
    trie_imported = pickle.loads(data)
    binary_file.close()
    return trie_imported


def bartez_trie_import_from_file(file, language):
    trie_dictionary = BartezDictionaryTrie(language)
    first = '0'

    with open(file) as f:
        for word in f:
            word = word.upper()
            word = word.replace("\n", "")
            word = word.replace("\r", "")

            if len(word) < 2:
                continue

            if word.isalpha() is False:
                continue

            if first != word[0]:
                first = word[0]
                print("adding page: " + str(first))

            trie_dictionary.add_word(word)

    return trie_dictionary


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
