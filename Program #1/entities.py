
import sys

def Abbr(word):
    if len(word) > 4 or (not word[0].isalpha() or word[-1] != "."):
        return 0
    else:
        newW = word.replace(".", "")
        if newW.isalpha():
            return 1
        else:
            return 0

def Cap(word):
    if word[0].isupper():
        return 1
    else:
        return 0

def getFeatures(file):
    fp = open(file, "r")
    lines = fp.readlines()
    lines.append("\n")

    labels = []
    vectors = []
    words = set()
    poss = set()

    prevW, prevP = "PHI", "PHIPOS"
    for line in lines:
        line = line.strip()
        if line == "":
            if prevW != "PHI":
                vectors[-1].extend((["OMEGA", "OMEGAPOS"]))
            prevW, prevP = "PHI", "PHIPOS"

        else:
            lList = line.split()
            #print(lList)
            labels.append(lList[0])
            word = lList[2]
            pos = lList[1]
            abbr = Abbr(word)
            cap = Cap(word)

            poss.add(pos)
            words.add(word)
            if prevW != "PHI":
                vectors[-1].extend([word, pos])

            vectors.append([word, pos, abbr, cap, prevW, prevP])
            prevW, prevP = word, pos

    if len(vectors[-1]) != 8:
        vectors[-1].extend(["OMEGA", "OMEGAPOS"])
    #vectors[-1].extend([None, None])
    for vec in vectors:
        if len(vec) != 8:
            print(vec)
    #print(len(labels), len(vectors), len(words))
    return labels, vectors, words, poss



def getFeatureTest(file, trainWords, trainPoss):
    fp = open(file, "r")

    #print(len(trainPoss))
    #print(trainPoss)
    lines = fp.readlines()
    lines.append("\n")

    labels = []
    vectors = []
    prevW, prevP = "PHI", "PHIPOS"
    for line in lines:
        line = line.strip()
        if line == "":
            if prevW != "PHI":
                vectors[-1].extend(["OMEGA", "OMEGAPOS"])
            prevW, prevP = "PHI", "PHIPOS"

        else:
            lList = line.split()
            labels.append(lList[0])
            word = lList[2]
            pos = lList[1]
            abbr = Abbr(word)
            cap = Cap(word)
            if word not in trainWords:
                #print(word)
                word = "UNK"
                #word, pos = "UNK", "UNKPOS"

            if pos not in trainPoss:
                pos = "UNKPOS"



            if prevW != "PHI":
                vectors[-1].extend([word, pos])
            vectors.append([word, pos, abbr, cap, prevW, prevP])
            prevW, prevP = word, pos


    if len(vectors[-1]) != 8:
        vectors[-1].extend(["OMEGA", "OMEGAPOS"])


    for i, vec in enumerate(vectors):
        if len(vec) != 8:
            print(i, vec)
    #print(len(vectors))
    return labels, vectors


def readableOutput(features, name, ftypes):

    output = open(name+".readable","w")
    #print(ftypes)

    for i in range(len(features)):

        if "WORD" in ftypes:
            output.write("WORD: "+str(features[i][0]) +"\n")
        else:
            output.write("WORD: n/a \n")

        if "POS" in ftypes:
            output.write("POS: " + str(features[i][1]) + "\n")
        else:
            output.write("POS: n/a \n")

        if "ABBR" in ftypes:
            if features[i][2] == 1:
                output.write("ABBR: yes"+"\n")
            else:
                output.write("ABBR: no" + "\n")
        else:
            output.write("ABBR: n/a \n")

        if "CAP" in ftypes:
            if features[i][3] == 1:
                output.write("CAP: yes" + "\n")
            else:
                output.write("CAP: no" + "\n")
        else:
            output.write("CAP: n/a \n")

        if "WORDCON" in ftypes:
            output.write("WORDCON: " + str(features[i][4]) + " " + str(features[i][6]) + "\n")
        else:
            output.write("WORDCON: n/a \n")

        if "POSCON" in ftypes:
            output.write("POSCON: " + str(features[i][5]) + " " + str(features[i][7]) + "\n")
        else:
            output.write("POSCON: n/a \n")

        output.write("\n")

def vectorOutput(labels, features, ftypes, featureIndex, labelIndex, featureID):


    vectors = []
    for i in range(len(labels)):

        label = labelIndex[labels[i]]

        vector = []

        for f in ftypes:
            idx = featureIndex[f]
            #print(i, key, idx)
            for k in idx:
                selectedFea = str(k)+str(features[i][k])

                if selectedFea in featureID:

                    vector.append(featureID[selectedFea])

        vector = sorted(vector)

        vectors.append([label]+vector)

    return vectors


def writeVectors(vectors, name):

    fp = open(name+".vector", "w")

    for i in range(len(vectors)):
        #print(vectors[1:])

        for j in range(len(vectors[i])):
            if j == 0:
                #fp.write(str(words[i][0]) + ": "+str(vectors[i][j]) + " ")
                fp.write(str(vectors[i][j]) + " ")
            else:
                fp.write(str(vectors[i][j]) + ":1" + " ")

        fp.write("\n")


def genFeatureID(ftypes, featureIndex, train_features):
    featureID = {}

    for f in ftypes:
        if f != "CAP" and f != "ABBR":
            idx = featureIndex[f]
            for k in idx:
                for i in range(len(train_features)):
                    feature = str(k)+str(train_features[i][k])
                    #print(feature)
                    if feature not in featureID:
                        featureID[feature] = len(featureID)+1

    featureID["0UNK"] = len(featureID)+1
    featureID["1UNKPOS"] = len(featureID)+1
    featureID["4UNK"] = len(featureID)+1
    featureID["6UNK"] = len(featureID)+1
    featureID["4UNKPOS"] = len(featureID)+1
    featureID["6UNKPOS"] = len(featureID)+1

    if "CAP" in ftypes:
        featureID["31"] = len(featureID)+1
    if "ABBR" in ftypes:
        featureID["21"] = len(featureID)+1

    return featureID



def main(args):

    train_file, test_file = args[0], args[1]

    ftypes = args[2:]


    train_labels, train_features, train_words, train_pos = getFeatures(train_file)

    test_labels, test_features = getFeatureTest(test_file, train_words, train_pos)

    #print(test_features)
    featureIndex = {"WORD": [0], "CAP": [3], "POS": [1], "ABBR": [2], "POSCON": [5, 7], "WORDCON":[4,6]}

    labelIndex = {"O": 0, "B-PER": 1, "I-PER": 2, "B-LOC": 3, "I-LOC":4, "B-ORG": 5, "I-ORG": 6}

    #if len(ftypes) == 1:

    readableOutput(train_features, train_file, ftypes)
    readableOutput(test_features, test_file, ftypes)


    featureID = genFeatureID(ftypes, featureIndex, train_features)

    #for w in train_words:
     #   if w not in featureID:
     #       featureID[w] = len(featureID) + 1
    #print(len(featureID))

    train_vectors = vectorOutput(train_labels, train_features, ftypes, featureIndex, labelIndex, featureID)
    #print(len(featureID))
    test_vectors = vectorOutput(test_labels, test_features, ftypes,  featureIndex, labelIndex, featureID)

    #print(len(featureID))
    #print(featureID)
    writeVectors(train_vectors, train_file)
    writeVectors(test_vectors, test_file)




if __name__ == "__main__":

    main(sys.argv[1:])