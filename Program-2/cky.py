
import argparse


def parse(grammar, sentence):
    words = sentence.split(" ")
    N = len(words)

    table = []

    for i in range(N):
        table.append([])
        for j in range(N):
            table[i].append({})

    for c in range(N):

        word = words[c]

        values = grammar[word]
        for term in values:
            if term[0] in table[c][c]:
                table[c][c][term[0]].append(float(term[1]))
            else:
                table[c][c][term[0]] = [float(term[1])]

        #print(c)
        for r in range(c-1, -1, -1):
            #print("r: "+str(r))
            for s in range(r+1, c+1):
                #print(r, s)
                B = table[r][s-1]

                C = table[s][c]

                for key_b in B.keys():
                    for key_c in C.keys():
                        key = key_b+" "+key_c
                        #print(B[key_b], C[key_c])
                        prob = float(max(B[key_b]))*float(max(C[key_c]))
                        if key in grammar:
                            for term in grammar[key]:
                                if term[0] in table[r][c]:
                                    table[r][c][term[0]].append(prob*float(term[1]))
                                else:
                                    table[r][c][term[0]] = [prob*float(term[1])]

    #print(table)
    return table


def printTable(sentence, table, output):
    output.write("PARSING SENTENCE: "+sentence +"\n")
    num = 0
    if "S" in table[0][-1]:
        num = len(table[0][-1]["S"])
    output.write("NUMBER OF PARSES FOUND: "+str(num)+"\n")
    output.write("TABLE:"+"\n")
    for i in range(len(table)):
        for j in range(i, len(table)):
            output.write("cell["+str(i+1)+","+str(j+1)+"]: ")
            if len(table[i][j]) == 0:
                output.write("-")
            else:
                terms = sorted(table[i][j].items(), key= lambda x: x[0])
                #print(terms)
                for term in terms:

                    for k in range(len(term[1])):
                        output.write(str(term[0])+" ")
            output.write("\n")
    output.write("\n")

def printTableProb(sentence, table, output):
    output.write("PARSING SENTENCE: "+sentence +"\n")
    num = 0
    if "S" in table[0][-1]:
        num = 1
    output.write("NUMBER OF PARSES FOUND: "+str(num)+"\n")
    output.write("TABLE:"+"\n")
    for i in range(len(table)):
        for j in range(i, len(table)):
            output.write("cell["+str(i+1)+","+str(j+1)+"]: ")

            if len(table[i][j]) == 0:
                output.write("-")
            else:
                terms = sorted(table[i][j].items(), key= lambda x: x[0])
                #print(terms)
                for term in terms:
                    output.write(str(term[0]) + "(" + str(format(max(term[1]), ".4f")) + ")" + " ")

            output.write("\n")
    output.write("\n")

def grammarCovert(grammar):
    fp = open(grammar)

    grammar_list = {}

    for line in fp.readlines():
        value = line.split("->")[0].strip()
        term = line.split("->")[1].split(".")[0].strip()
        prob = line.split("->")[1].split()[-1]
        if term not in grammar_list:
            grammar_list[term] = [[value, prob]]
        else:
            grammar_list[term].append([value, prob])


    return grammar_list

def main(grammar, sfile, prob):
    fp = open(sfile)

    if prob:
        proboutput = open(sfile + ".probcky", "w")
    else:
        output = open(sfile + ".cky", "w")

    grammar_list = grammarCovert(grammar)

    for line in fp.readlines():
        line = line.strip()
        if line != "":
            line = line.strip("\n")

            table = parse(grammar_list, line)

            if prob:
                printTableProb(line, table, proboutput)
            else:
                printTable(line, table, output)




if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("grammar", help="PCFG file", type=str)
    argparser.add_argument("sentences", help="sentences file", type=str)
    argparser.add_argument("-prob", "--prob", help="CKY with probability", action="store_true")
    args = argparser.parse_args()

    main(args.grammar, args.sentences, args.prob)