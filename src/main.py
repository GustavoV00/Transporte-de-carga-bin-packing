# Gustavo Valente Nunes
# GRR 20182557

import simplex as sp
import branchAndBound as bd

def main():
    variablesAmount = 0
    otimo = 0
    level = 0

    [solver, variablesAmount, y, x, data] = sp.restricoes(variablesAmount)

    result = bd.branchAndBound(level, x, y, otimo, variablesAmount, solver, data)
    print(result)

if __name__ == "__main__":
    main()
