#!/usr/bin/python3

from ortools.linear_solver import pywraplp
import sys


def addDependencesToDict(dependences, inputs):

    i = 0
    while(i < len(dependences)):
        item = (dependences[i], dependences[i+1])    
        inputs["ordered_pairs"].append(item)
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

def create_model():
    data = {}
    
    # Dicionario que salvo os dados de entrada 
    # a partir do arquivo.
    dictInput = {
        "firstLine": [],
        "weights": [],
        "ordered_pairs": [],
    }

    leInputs(dictInput)

    # Indica os pesos de cada item
    data["weights"] = dictInput["weights"]

    # Indica a quantidade de itens existentes
    # Será utilizado para criar as váriaveis mais tarde
    data["items"] = list(range(len(dictInput["weights"])))

    # Indica a quantidade de caminhões.
    data["trucks"] = data["items"]

    # Indica os pares ordenados. Aviso: Não foi utilizado.
    data["ordered_pairs"] = dictInput["ordered_pairs"]

    #Indica a capacidade da carga, C
    data["bin_capacity"] = dictInput["firstLine"][2]


    return data;

def main():
    # Faz a modelagem dos dados dentro de um dicionário.
    data = create_model()

    # Escolhe o resolvedor, o GLOP é um desses resolvedores. 
    solver = pywraplp.Solver('binPacking',
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Criação das váriaveis #


    # x[i, j] = 1, se o item está no caminhão j
    x = {}
    for i in data['items']:
        for j in data['trucks']:
            # Cria uma váriavel(objeto do tipo NumVar) e salvo na váriavel x_i_j
            x[(i, j)] = solver.NumVar(0.0, 1.0, 'x_%i_%i' % (i, j))



    # y[j] = 1, se o caminhão j está sendo usado. 
    y = {}
    for j in data['trucks']:
        y[j] = solver.NumVar(0.0, 1.0, 'y[%i]' % j)


    # Restrições #


    # A soma dos itens existentes, não devem exceder 1. 
    # Isso porque, a soma dos itens não deve exceder o caminhão. 
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['trucks']) == 1)



    # Indica que o peso não deve exceder a capacidade 
    for j in data['trucks']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items'])  <= data["bin_capacity"]*y[j]
        )


    # Função objetiva. Minimza o numero de caminhões utilizados.
    solver.Minimize(solver.Sum([y[j] for j in data['trucks']]))

    # Chama o resolver
    solver.Solve()

    # Imprime os resultados na tela. 
    print("Object value = ", solver.Objective().Value())
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

if __name__ == "__main__":
    main()
