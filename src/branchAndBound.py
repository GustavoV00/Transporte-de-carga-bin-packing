from ortools.linear_solver import pywraplp

def optimalSolution(solver, y, x, data, novasRes, level):
    # Função objetiva. Minimza o numero de caminhões utilizados.
    i = 0
    while(i < len(novasRes) and novasRes[i] != -1):
        print("AAAAAAAAAAAAAA: %d e %d" % (level, novasRes[i]))
        solver.Add(x[novasRes[i], level] == 1)
        i += 1

    solver.Minimize(solver.Sum([y[j] for j in data['trucks']]))

    status = solver.Solve()

    ramifica = True;
    if status == pywraplp.Solver.OPTIMAL:
        num_bins = 0.
        for j in data['trucks']:
            # print(f"y[{j}]",y[j].solution_value())
            if y[j].solution_value() >= 0:
                bin_items = []
                bin_weight = 0
                for i in data['items']:
                    # print(f"x[{i}, {j}]",x[i,j].solution_value())
                    if(x[i,j].solution_value() < 1 and x[i,j].solution_value() > 0):
                        ramifica = True

                    bin_items.append(i)
                    bin_weight += data['weights'][i]
                # print()
                # if bin_weight >= 0:
                #     num_bins += 1
                #     print('Bin number', j)
                #     print('  Items packed:', bin_items)
                #     print('  Total weight:', bin_weight)
                #     print()
        # print()
        # print('Number of bins used:', num_bins)
        # print('Time = ', solver.WallTime(), ' milliseconds')
    else:
        ramifica = False
        print('The problem does not have an optimal solution.\n')

    otimo = -1
    if(ramifica == True):
        otimo = solver.Objective().Value()

    return [ramifica, otimo]


def branchAndBound(solver, variablesAmount, otimo, level, itens, y, x, data, ramifica, novasRes, i):

    # TENTAR FAZER ESSA SOLUÇÃO, UTILIZANDO UMA FORMA DE REMOVER O ELEMENTO DA LISTA E INSERIR NOVAMENT
    if(level == 0):
        [ramifica, otimo] = optimalSolution(solver, y, x, data, novasRes, level)
        print('LEVEL: ', level)
        print('ITENS:', itens)
        print("NOVAS RES: ", novasRes)
        print("Otimo: ", otimo)
        print()
        if(ramifica == True):
            for i in range(len(itens)):
                otimo = branchAndBound(solver, variablesAmount, otimo, level+1, itens, y, x, data, ramifica, novasRes, i)

        else:
            return otimo

    elif (level < variablesAmount):
        [ramifica, otimo] = optimalSolution(solver, y, x, data, novasRes, level)
        if(ramifica == True):
            i = 0
            while(i < len(itens)):
                aux = itens[i]
                novasRes[level-1] = aux
                del itens[i]
                print('LEVEL: ', level)
                print('ITENS:', itens)
                print("NOVAS RES: ", novasRes)
                print("Otimo: ", otimo)
                print()
                otimo = branchAndBound(solver, variablesAmount, otimo, level+1, itens, y, x, data, ramifica, novasRes, i)
                itens.insert(i, aux)
                novasRes[level] = -1
                i += 1
    else:
        novasRes[level-1] = itens[0]
        print('LEVEL: ', level)
        print('ITENS:', itens)
        print("NOVAS RES: ", novasRes)
        print("iTem: ", i)
        print("Otimo: ", otimo)
        print()
        [ramifica, otimo] = optimalSolution(solver, y, x, data, novasRes, level)
        return otimo

    return otimo;
