import random

def load_dictionary_from_file(word_list_file):
    dictionary = []

    count = 0

    with open(word_list_file) as f:
        for word in f:
            count = count + 1
            word = word.replace("\n", "")
            word = word.replace("\r", "")

            if word.isalpha() is False:
                continue

            if len(word) < 2:
                continue

#            if count % 10 != 0:
#                continue

            difference = len(word) - len(dictionary) + 1
            if difference > 0:
                for p in range(0, difference):
                    dictionary.append([])

            dictionary[len(word)].append((word.upper()))
    return dictionary

def shuffle_words(dictionary):
    for page_index, page in enumerate(dictionary):
        random.shuffle(page)

def make_dictionary_matrix(dictionary, max_word_length):

    matrix = []
    domain_ranges = {}

    for page_index, page in enumerate(dictionary):
        if page_index < 2 :
            continue

        if len(page) == 0:
            continue

        if page_index > max_word_length:
            continue

        domain_start = len(matrix)

        for word in page:
            assert (page_index == len(word))
            padding_length = max_word_length - page_index
            word_to_int = ( [ord(letter) for letter in word] )
            word_to_int = [ i - (ord('A') - 1) for i in word_to_int ]
            word_to_int = word_to_int + [0 for _ in range(padding_length)]
            matrix.append(word_to_int)

        domain_end = len(matrix) - 1
        domain_ranges[page_index] = (domain_start, domain_end)

    return matrix, domain_ranges

def main():
    word_list_file = "words.txt"
    dictionary = load_dictionary_from_file(word_list_file)
    matrix, domain = make_dictionary_matrix(dictionary, 5)

    print (domain)

    return

if __name__ == "__main__":
  main()
