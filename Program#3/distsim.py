import argparse
from numpy import inner
from numpy.linalg import norm
import collections


def stopWord(file):
    fp = open(file, "r")
    stop_words = set()
    for word in fp.readlines():
        word = word.strip()
        stop_words.add(word)
    return stop_words


def getGold_words(file, k, Senses, feature_idx):
    
    definitions = {}
    for s in Senses:
        definitions[s] = [0]*len(feature_idx)
    
    fp = open(file, "r")
    for line in fp.readlines():
        sense = line.split("\t")[0].split(":")[1]
        line = line.split("\t")[1]
        left_part = (line.split("<occurrence>")[0].strip()).split()[::-1]
        if len(left_part) > k:
            left_part = left_part[:k]
        right_part = (line.split("</>")[1].strip()).split()
        if len(right_part) > k:
            right_part = right_part[:k]

        all_parts = left_part +right_part 
        
        for w in all_parts:
            w = w.lower()
            if w in feature_idx:
                idx = feature_idx[w]
                definitions[sense][idx] += 1
                                       
    return definitions


def convert_words_vector(line, k, feature_label):
    
    vector = [0]*len(feature_label)
    
    left_part = (line.split("<occurrence>")[0].strip()).split()[::-1]
    right_part = (line.split("</>")[1].strip()).split()

    if len(left_part) > k:
        left_part = left_part[:k]
    if len(right_part) > k:
        right_part = right_part[:k] 

    all_parts = left_part +right_part 

    for w in all_parts:
        w = w.lower()
        if w in feature_label:
            idx = feature_label[w]
            vector[idx] += 1          
    return vector

def similarity(vector, definitions_vectors):

    similar = {}

    for d in definitions_vectors.keys():
        dvector = definitions_vectors[d]
        cos_sim = inner(vector, dvector)/(norm(vector)*norm(dvector))
        similar[d] = cos_sim

    return similar



def get_allWords(file, k, stop_words):
    
    fp = open(file,"r")
    onewords = set()
    output = set()
    #targets = set()
    numTrain = 0
    
    Senses = set()
    for line in fp.readlines():
        numTrain += 1
        sense = line.split("\t")[0].split(":")[1]
        Senses.add(sense)
        line = line.split("\t")[1]
        left_part = (line.split("<occurrence>")[0].strip()).split()[::-1]

        right_part = (line.split("</>")[1].strip()).split()
        if len(left_part) > k:
            left_part = left_part[:k]
        if len(right_part) > k:
            right_part = right_part[:k] 
        
        all_parts = left_part +right_part 
        
        for w in all_parts:
            w = w.lower()
            if any(c.isalpha() for c in w) and w not in stop_words:
                if w in onewords:
                    output.add(w)
                else:
                    onewords.add(w)
                    
    return numTrain, Senses, output



def main(train_file, test_file, stop_file, k):
    if k== 0:
        k = float("inf")
    
    output = open(test_file+".distsim", "w")
    stop_words = stopWord(stop_file)
    
    numTrain, Senses, words = get_allWords(train_file, k, stop_words)

    feature_label = {}
    words = list(words)
    for w in range(len(words)):
        feature_label[words[w]] = w
    #print(feature_label)
    definitions = getGold_words(train_file, k, Senses, feature_label)


    test_fp = open(test_file, "r")


    test_lines = test_fp.readlines()
    
    output.write("Number of Training Sentences = "+str(numTrain))
    output.write("\n")
    output.write("Number of Test Sentences = "+str(len(test_lines)))
    output.write("\n")
    output.write("Number of Gold Senses = "+str(len(definitions)))
    output.write("\n")
    output.write("Vocabulary Size = "+str(len(words)))
    output.write("\n")
    

    for line in test_lines:
        line_vector = convert_words_vector(line, k, feature_label)
        similar_values = similarity(line_vector, definitions)
        similar_values = sorted(similar_values.items(), key=lambda x:(-x[1], x[0]))
        #print(similar_values)
        for item in similar_values:
            output.write(str(item[0])+"("+str(format(item[1], ".2f"))+") ")
        output.write("\n")
        



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("train_file", help="train_file", type=str)
    argparser.add_argument("test_file", help="test_file", type=str)
    argparser.add_argument("stop_file", help="stop_file", type=str)
    argparser.add_argument("k", help="parameter k", type=int)
    args = argparser.parse_args()

    main(args.train_file, args.test_file, args.stop_file, args.k)