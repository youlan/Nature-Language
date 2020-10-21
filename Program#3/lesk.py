
import argparse

def stopWord(file):

    fp = open(file, "r")
    stop_words = set()
    for word in fp.readlines():
        word = word.strip()
        stop_words.add(word)
    return stop_words

def convertDefinition(file, stopwords):
    fp = open(file,"r")
    definitions = {}
    for line in fp.readlines():
        terms = line.strip().split("\t")
        #print(terms)
        words = set()
        for term in terms[1:]:
            for w in term.split(" "):
                w = w.lower()
                if any(c.isalpha() for c in w) and w not in stopwords:
                    words.add(w)
        definitions[terms[0]] = words
    return definitions

def sentence_analysis(line, stopwords):
    target = line.split("<occurrence>")[1].split("</>")[0]
    first_part = line.split("<occurrence>")[0]
    second_part = line.split("</>")[1]
    all_part =first_part+second_part

    words = set()
    for w in all_part.split(" "):
        w = w.lower()
        if any(c.isalpha() for c in w) and w not in stopwords:
            words.add(w)

    return target.lower(), words


def main(test_file, definitions, stop_file):

    stop_words = stopWord(stop_file)
    #print(stop_words)
    definitions_dicts = convertDefinition(definitions, stop_words)

    #target_words = get_targetWords(test_file)

    output = open(test_file+".lesk", "w")

    test_fp = open(test_file,"r")


    for line in test_fp.readlines():
        target, words = sentence_analysis(line, stop_words)

        freq = {k:0 for k in definitions_dicts.keys()}

        for k in definitions_dicts.keys():
            define_word = definitions_dicts[k]
            intersection = define_word.intersection(words)
            freq[k] += len(list(intersection))
        sentence_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

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