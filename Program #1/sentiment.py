


import sys


def getSentences(fp):
    fp = open(fp, "r")
    lines = fp.readlines()
    lines.append("\n")
    sentences = []
    sentence = []
    for line in lines:
        word = line.strip()
        if word == '':
            if len(sentence) > 0:
                sentences.append(sentence)
            sentence = []
        else:
            sentence.append(word)
    #if len(sentence) != 0:
    #    sentences.append((sentence))
    print(len(sentences))
    return sentences


def getKwords(fp, k):
    featureFile = open(fp, "r")

    kWords = []

    for i in range(k):
        word = featureFile.readline().strip()
        while word == "":
            word = featureFile.readline()
        kWords.append(word)
    return kWords

def getFVectors(sentences, kWords):

    Vectors = []

    for i in range(len(sentences)):
        temp = [sentences[i][0]]
        #print(sentences[i])
        #print(sentences[i][1:])
        for k in range(len(kWords)):
            word = kWords[k]

            if word in sentences[i][1:]:
                temp.append(k+1)
        #print(len(Vectors[i])
        Vectors.append(temp)
    #print(Vectors)
    return Vectors


def exportVectors(vectors, name):

    output = open(name+".vector","w")

    for i in range(len(vectors)):
        #print(vectors[i])
        output.write(str(vectors[i][0])+' ')
        #print(vectors[i])
        for k in range(1, len(vectors[i])):
            #if vectors[i][k] == 1:
            output.write(str(vectors[i][k]) +":"+str(1)+" ")
        output.write("\n")





def main(args):

    train_file, test_file, features_file, k = args[0], args[1], args[2], int(args[3])
    train_Sent = getSentences(train_file)
    test_Sent = getSentences(test_file)

    kWords = getKwords(features_file, k)

    train_Vectors = getFVectors(train_Sent, kWords)
    test_Vectors = getFVectors(test_Sent, kWords)

    exportVectors(train_Vectors, train_file)
    exportVectors(test_Vectors, test_file)



if __name__ == "__main__":
    main(sys.argv[1:])