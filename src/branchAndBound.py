from collections import deque
from ortools.linear_solver import pywraplp


class Pack:
    def __init__(self, level, x, y, otimo, variablesAmount, solver, data):
        self.level = level
        self.maxLevel = variablesAmount
        self.x = x
        self.y = y
        self.novasRes = [ -1 for _ in range(variablesAmount)]
        self.itens = [(a) for a in range(variablesAmount) ]
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

        # Adicionar restrições extras

        # Bound
        self.solver.Minimize(self.solver.Sum([self.y[j] for j in self.data['trucks']]))

        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            # Se não tivermos um resultado ótimo inteiro, ramificamos mais
            if(type(bd) == int):
                    bd = False

            bd = self.verificaSeOsItensEstaoInteiros()
        else:
            # Se cairmos em um caso em que não existe nenhuma solução viável, não limitamos mais
            self.otimo = -1
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
    p1 = Pack(level, x, y, otimo, variablesAmount, solver, data)
    SOLUCAO_OTIMA = -1

    queue = deque()
    queue.append(p1)


    while(len(queue) != 0):
        u = queue.popleft()

        if(u.level == u.maxLevel):
            continue

        if(u.ramifica(SOLUCAO_OTIMA)):
            for i in range(len(u.itens)):
                v = Pack(u.level+1, x, y, otimo, variablesAmount, solver, data)
                aux = v.itens[i]
                del v.itens[i]
                v.novasRes[u.level] = aux
                print("LEVEL: ", v.level)
                print("ITENS: ", v.itens)
                print("novasRes: ", v.novasRes)
                print("\n\n")
                queue.append(v)
                
    return SOLUCAO_OTIMA;
