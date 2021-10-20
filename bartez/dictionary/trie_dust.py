from dustpy import Trie, TrieWithPagesByLength, TrieWithPagesByLengthRobinMap, TrieWithPagesByLengthHopscotchMap

class DustDictionaryTriePatternMatcher(object):

    def __init__(self, trie):
        self.__trie = trie


    def add_word(self, word):
        if len(word) < 2:
            return
        self.__trie.add_word(word)


    def remove_word(self, word):
        self.__trie.remove_word(word)


    def get_matches(self, pattern):
        return self.__trie.find(pattern)



def dust_trie_import_from_file(file, wildcard, terminator):
    t = TrieWithPagesByLengthHopscotchMap(ord(wildcard), ord(terminator))
    trie_dictionary = DustDictionaryTriePatternMatcher(t)
#    first = '0'

    with open(file) as f:
        for word in f:
            word = word.replace("\n", "")
            word = word.replace("\r", "")
            word = word.upper()
            if len(word) < 2:
                continue

            trie_dictionary.add_word(word)

    return trie_dictionary



def ImportTest(trie):
    trie.add_word("test")
    results = trie.find("t...")
    for _, rss in enumerate(results):
        print(rss)

def DoImportTest():
    ImportTest(Trie())
    ImportTest(TrieWithPagesByLength())
    ImportTest(TrieWithPagesByLengthRobinMap())
    ImportTest(TrieWithPagesByLengthHopscotchMap())

DoImportTest()
