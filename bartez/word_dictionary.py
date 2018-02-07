class DictionaryEntry:
    def __init__(self, word, definitions):
        self.__word = word
        self.definitions = definitions

    def get(self):
        return self.__word


class Dictionary:
    def __init__(self, language, dictionary_file):
        self.__language = language
        self.__file = dictionary_file
        self.__d = []
        self.__load()

    def get_language(self):
        return self.__language

    def get_page_count(self):
        return len(self.__d)

    def get_page(self, num):
        """page num corresponds to words length collected in that page"""
        if num >= self.get_page_count():
            return []

        return self.__d[num]

    def get_words_count(self):
        words_count = 0
        for page in self.__d:
            words_count += len(page)
        return words_count

    def __load(self):
        with open(self.__file) as f:
            for word in f:
                word = word.replace("\n", "")
                word = word.replace("\r", "")
                difference = len(word) - len(self.__d)
                if difference > 0:
                    for p in range(0, difference):
                        self.__d.append([])

                self.__d[len(word)-1].append(DictionaryEntry(word.upper(), []))
