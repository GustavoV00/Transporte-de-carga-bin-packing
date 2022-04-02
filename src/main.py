from scipy.optimize import linprog
import numpy as np
import sys

def addDependencesToDict(dependences, inputs):

    i = 0
    while(i < len(dependences)):
        item = (dependences[i], dependences[i+1])    
        inputs["conditions"].append(item)
        i += 2

def leInputs(inputs):
    # Lê do stdin
    dependences = []
    i = 0
    for line in sys.stdin:
        #Coloca os valores em um vetor chamado inputs
        for word in line.split():
            if (i == 0):
                inputs["firstLine"].append(int(word))
            elif(i == 1):
                inputs["weights"].append(int(word))
            else:
                dependences.append(int(word))

        i += 1


    addDependencesToDict(dependences, inputs)
    return inputs

def creatingObjectFunction(c, total):
    for _ in range(total):
        c.append(1)


def subjectToLeftSide(n, linearProg, weights):

    aux = []
    for _ in range(n):
        for j in range(n):
            aux.append(weights[j])
    
        print("aux: ", aux)
        linearProg["restrictions"]["leftSide"].append(aux)
        linearProg["restrictions"]["rightSide"].append(10)
        aux.clear()

def main():
    dictInput = {
        "firstLine": [],
        "weights": [],
        "conditions": [],
    }

    linearProg = {
        "min": [],
        "restrictions": {
            "leftSide": [],
            "rightSide": [],
        }
    }

    leInputs(dictInput)
    print("DictInput: ", dictInput)
    print("\n")

    # y_i -> Pacote i
    totalBins = dictInput["firstLine"][0]
    # print(totalBins)

    creatingObjectFunction(linearProg["min"], totalBins)

    subjectToLeftSide(totalBins, linearProg, dictInput["weights"])
    print("LinearProg: ", linearProg)


if __name__ == "__main__":
    main()
