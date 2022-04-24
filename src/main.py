# Gustavo Valente Nunes
# GRR 20182557

import simplex as sp
import branchAndBound as bd



def main():
    variablesAmount = 0
    otimo = 0
    level = 0
    ramifica = True
    [solver, variablesAmount, y, x, data] = sp.restricoes(variablesAmount)

    novasRes = [ -1 for _ in range(variablesAmount)]
    itens = [(a) for a in range(variablesAmount) ]
    result = bd.branchAndBound(solver, variablesAmount, otimo, level, itens, y, x, data, ramifica, novasRes, 0)
    print(result)

if __name__ == "__main__":
    main()
