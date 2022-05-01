from ortools.linear_solver import pywraplp
import inputs as ip

def create_model(variablesAmount):
    data = {}
    
    # Dicionario que salvo os dados de entrada 
    # a partir do arquivo.
    dictInput = {
        "firstLine": [],
        "weights": [],
        "ordered_pairs": [],
    }

    ip.leInputs(dictInput)
    variablesAmount = dictInput["firstLine"][0]

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
    data["trucks_capacity"] = dictInput["firstLine"][2]


    return [data, variablesAmount];

def restricoes(variablesAmount, novasRes, itens, data, level):
    # Faz a modelagem dos dados dentro de um dicionário.
    if(novasRes == None and itens == None and data == None):
        [data, variablesAmount] = create_model(variablesAmount)

    # Escolhe o resolvedor, o GLOP é um desses resolvedores. 
    solver = pywraplp.Solver('trucksPacking',
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Criação das váriaveis #


    # x[i, j] = 1, se o item está no caminhão j
    x = {}
    for i in data['items']:
        for j in data['trucks']:
            # Cria uma váriavel(objeto do tipo NumVar) e salvo na váriavel x_i_j
            x[(i, j)] = solver.NumVar(0, 1, 'x_%i_%i' % (i, j))



    # y[j] = 1, se o caminhão j está sendo usado. 
    y = {}
    for j in data['trucks']:
        y[j] = solver.NumVar(0, 1.0, 'y[%i]' % j)


    # Restrições #


    # A soma dos itens existentes, não devem exceder 1. 
    # Isso porque, a soma dos itens não deve exceder o caminhão. 
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['trucks']) == 1)


    # Indica que o peso não deve exceder a capacidade 
    for j in data['trucks']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items'])  <= data["trucks_capacity"]*y[j]
        )

    if(novasRes != None and itens != None and data != None):
        # Adicionar restrições extras de forma dinamica, de acordo com o level da árvore
        i = 0
        for l in range(level):
            print("AAAAAAAAAAAAAA: x[%d, %d]" % (novasRes[i], l))
            solver.Add(x[novasRes[i], l] == 1)
            i += 1

    solver.Minimize(solver.Sum([y[j] for j in data['trucks']]))

    return [solver, variablesAmount, y, x, data];
