from collections import deque
import simplex as sp
from ortools.linear_solver import pywraplp


class Pack:
    def __init__(self, level, x, y, otimo, variablesAmount, solver, data, novasRes, itens):
        self.level = level
        self.maxLevel = variablesAmount
        self.x = x
        self.y = y
        self.novasRes = [ elem for elem in novasRes]
        self.itens = [item for item in itens ]
        self.otimo = otimo
        self.variablesAmount = variablesAmount
        self.solver = solver
        self.data = data

    def verificaSeOsItensEstaoInteiros(self):
        i = 0
        j = 0
        k = 0
        while(k < len(self.x)):
            if(type(self.x[i,j].solution_value()) != int):
                return False
            k += 1

        return True
                

    def bound(self):
        bd = True

        # Bound
        if(self.level > 0):
            [self.solver, self.variablesAmount, self.y, self.x, self.data] = sp.restricoes(self.variablesAmount, self.novasRes, self.itens, self.data, self.level)
            status = self.solver.Solve()
        else:
            status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("EXISTE SOLUCAO ÓTIMA VIÁVEL")
            self.otimo = self.solver.Objective().Value()

            # Se não tivermos um resultado ótimo inteiro, ramificamos mais
            if(type(self.otimo) == int):
                    bd = False

            bd = self.verificaSeOsItensEstaoInteiros()

        else:
            # Se cairmos em um caso em que não existe nenhuma solução viável, não limitamos mais
            print("NÃO EXISTE SOLUCAO VIÁVEL\n\n\n\n")
            self.otimo = -2
            bd = False
        
        # Se for False, ramifica. Se for True não ramifica
        return bd

    def ramifica(self, SOLUCAO_OTIMA):
        ramifica = False

        if(not self.bound()):
            ramifica = True
        else:
            if(SOLUCAO_OTIMA < self.otimo):
                self.otimo = SOLUCAO_OTIMA

        return ramifica

def branchAndBound(level, x, y, otimo , variablesAmount, solver, data):
    novasRes = [ -1 for _ in range(variablesAmount)]
    itens = [(a) for a in range(variablesAmount) ]
    p1 = Pack(level, x, y, otimo, variablesAmount, solver, data, novasRes, itens)
    SOLUCAO_OTIMA = -1

    queue = deque()
    queue.append(p1)


    id = 0
    while(len(queue) != 0):
        u = queue.popleft()

        if(u.ramifica(SOLUCAO_OTIMA)):
            for i in range(len(u.itens)):
                v = Pack(u.level+1, x, y, otimo, variablesAmount, solver, data, u.novasRes, u.itens)
                aux = v.itens[i]
                del v.itens[i]
                v.novasRes[u.level] = aux
                queue.append(v)
                
        print("LEVEL: ", u.level)
        print("id: ", id)
        print("ITENS: ", u.itens)
        print("novasRes: ", u.novasRes)
        print("otimo: ", u.otimo)
        print("\n\n")
        id += 1
    return SOLUCAO_OTIMA;
