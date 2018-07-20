from bartez.dictionary.trie_serializer import serialize_pattern_matcher
import sys

def main():
    args = sys.argv[1:]
    if len(args) != 3:
        return 1

    print("Serializing pattern matcher")
    file_src = sys.argv[1]
    language = sys.argv[2]
    matcher_file = sys.argv[3]
    print("file src: " + file_src)
    print("language: " + language)
    print("matcher file: " + matcher_file)

    serialize_pattern_matcher(file_src, language, matcher_file)
    print("Serialization complete")


if __name__ == "__main__":
    main()
