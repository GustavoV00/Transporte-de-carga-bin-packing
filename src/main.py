# Gustavo Valente Nunes
# GRR 20182557

import simplex as sp
import branchAndBound as bd

def main():
    variablesAmount = 0
    otimo = 0
    level = 0

    [solver, variablesAmount, y, x, data, _] = sp.restricoes(variablesAmount, None, None, None, level)

    result = bd.branchAndBound(level, x, y, otimo, variablesAmount, solver, data)
    if result == -1:
        print("Não foi encontrado nenhum resultado otimo inteiro")
    else:
        print(result)

if __name__ == "__main__":
    main()
