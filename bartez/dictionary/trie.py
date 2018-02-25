from bartez.dictionary.trie_node import BartezNodeTerminal, BartezNodeNonTerminal


class BartezTrie(object):
    """Bartez trie, used by dictionary"""

    def __init__(self, language, file):
        self.__language = language
        self.__file = file
        self.__root = None
        self.__load()


    def get_language(self):
        return self.__language


    def get_file(self):
        return self.__file


    def get_root(self):
        return self.__root


    def is_loaded(self):
        return self.__root is not None


    def add_word(self, word):
        if self.is_loaded() is False:
            return

        parent = self.__root
        child = None
        for pos in range(len(word)):
            current_char = word[pos]
            child = parent.get_child(current_char)
            if child == None:
                child = BartezNodeNonTerminal(parent, current_char)
                parent.add_child(child)

            parent = child

        if parent.has_terminal() == False:
            child = BartezNodeTerminal(parent)
            parent.add_child(child)

    def __load(self):
        if self.__root == None:
            self.__root = BartezNodeNonTerminal(None, '')

        first = '0'

        with open(self.__file) as f:
            for word in f:
                word = word.replace("\n", "")
                word = word.replace("\r", "")

                if len(word) < 2:
                    continue

                if first != word[0]:
                    first = word[0]
                    print("adding page: " + str(first))
                    
                
                self.add_word(word.upper())
