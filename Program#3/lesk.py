
import argparse

def stopWord(file):

    fp = open(file, "r")
    stop_words = set()
    for word in fp.readlines():
        word = word.strip()
        stop_words.add(word)
    return stop_words

def filterSW(sentence, stopwords):
    words = set(sentence)
    return words- stopwords


def convertDefinition(file, stopwords):
    fp = open(file,"r")
    definitions = {}
    for line in fp.readlines():
        terms = line.strip().split("\t")
        #print(terms)
        words = []
        for term in terms:
            for w in term.split(" "):
                if w.isalpha():
                    words.append(w.lower())

        wordSet = filterSW(words, stopwords)
        #print(wordSet)
        definitions[terms[0]] = wordSet
    return definitions

def sentence_analysis(line, stopwords):
    target = line.split("<occurrence>")[1].split("</>")[0]
    first_part = line.split("<occurrence>")[0]
    second_part = line.split("</>")[1]
    all_part =first_part+second_part

    words = set()
    for w in all_part.split(" "):
        if w.isalpha():
            words.add(w.lower())

    return target.lower(), filterSW(words, stopwords)

def get_targetWords(test_file):
    fp = open(test_file, "r")

    target_words = set()
    for line in fp.readlines():
        target = line.split("<occurrence>")[1].split("</>")[0]
        target_words.add(target.lower())
    return target_words



def main(test_file, definitions, stop_file):

    stop_words = stopWord(stop_file)
    #print(stop_words)
    definitions_dicts = convertDefinition(definitions, stop_words)

    target_words = get_targetWords(test_file)

    output = open(test_file+".lesk", "w")

    test_fp = open(test_file,"r")


    for line in test_fp.readlines():
        target, words = sentence_analysis(line, stop_words)

        freq = {k:0 for k in definitions_dicts.keys()}

        for k in definitions_dicts.keys():
            define_word = definitions_dicts[k]
            intersection = define_word.intersection(words)-target_words
            freq[k] += len(list(intersection))
        sentence_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
        print(sentence_freq)
        for item in sentence_freq:
            output.write(str(item[0])+"("+str(item[1])+") ")
        output.write("\n")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("test_file", help="test_file", type=str)
    argparser.add_argument("definitions", help="definitions", type=str)
    argparser.add_argument("stop_file", help="stop_file", type=str)
    args = argparser.parse_args()

    main(args.test_file, args.definitions, args.stop_file)