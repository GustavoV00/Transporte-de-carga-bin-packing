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


def subjectTo(n, linearProg, weights, capacity):

    aux = []
    for _ in range(n):
        linearProg["restrictions1"]["leftSide"].append(weights)
        linearProg["restrictions1"]["rightSide"].append(capacity)
        aux.append(1)
    
    for _ in range(n):
        linearProg["restrictions2"]["leftSide"].append(aux)
        linearProg["restrictions2"]["rightSide"].append(1)
        


def lessBound(n, restrictions):

    A_ub = []
    while(n < len(restrictions)):
        A_ub.append(restrictions[n])
        n += 1
    
    return A_ub

def bounds(n):
    bounds = []
    for _ in range(n):
        bounds.append((0, 1))
        
    return bounds

def main():
    dictInput = {
        "firstLine": [],
        "weights": [],
        "conditions": [],
    }

    linearProg = {
        "min": [],
        "restrictions1": {
            "leftSide": [],
            "rightSide": [],
        },
        "restrictions2": {
            "leftSide": [],
            "rightSide": [],
        },
    }

    leInputs(dictInput)
    # print("DictInput: ", dictInput)
    # print("\n")

    # y_i -> Pacote i
    totalBins = dictInput["firstLine"][0]
    # print(totalBins)

    creatingObjectFunction(linearProg["min"], totalBins)

    capacity = dictInput["firstLine"][2]
    subjectTo(totalBins, linearProg, dictInput["weights"], capacity)
    # print("LinearProg: ", linearProg)

    c = np.array(linearProg["min"])
    A_ub = linearProg["restrictions1"]["leftSide"]
    b_ub = linearProg["restrictions1"]["rightSide"]

    A_eq = linearProg["restrictions2"]["leftSide"]
    b_eq = linearProg["restrictions2"]["rightSide"]


    bd = bounds(totalBins)
    print(c, "\n")
    print(A_ub, " <= ", b_ub, "\n")
    print(A_eq, " = ", b_eq, "\n")
    print(bd, "\n")

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(bd))
    print(res, "\n")


if __name__ == "__main__":
    main()
