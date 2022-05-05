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
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                if(type(self.x[i, j].solution_value()) != int):
                    return False

        return True

    def bound(self):
        # Indica que o resultado encontrado foi inteiro
        # E os x_i foram todos inteiros
        bd = True

        # Bound
        ordenado = None
        if(self.level > 0):
            [self.solver, self.variablesAmount, self.y, self.x, self.data, ordenado] = sp.restricoes(self.variablesAmount, self.novasRes, self.itens, self.data, self.level)

        # Limitante
        if(ordenado == True or self.level == 0):
            self.solver.Minimize(self.solver.Sum([self.y[j] for j in self.data['trucks']]))
            status = self.solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                # print("EXISTE SOLUCAO ÓTIMA VIÁVEL")
                self.otimo = self.solver.Objective().Value()


                # Se existir algum numero fracionário, continuamos a ramificar 
                bd = self.verificaSeOsItensEstaoInteiros()

                # Se não tivermos um resultado ótimo inteiro, ramificamos mais
                if(type(self.otimo) == int):
                    bd = False

            else:
                # Se cairmos em um caso em que não existe nenhuma solução viável, não limitamos mais
                print("NÃO EXISTE SOLUCAO VIÁVEL\n\n\n\n")
                self.otimo = -2
                bd = False


        # Se for False, ramifica. Se for True não ramifica
        # print(bd)
        return bd

    def ramifica(self, SOLUCAO_OTIMA):
        ramifica = True


        
        # Se bound() devolver falso, significa que é preciso ramificar
        # Se bound() devolver verdadeiro, encontrei um resultado ótimo.
        if(self.bound() == True):
            ramifica = False

        if(self.level == 0):
            self.otimo = SOLUCAO_OTIMA
            
        if(self.otimo < SOLUCAO_OTIMA and type(self.otimo) == int):
            SOLUCAO_OTIMA = self.otimo
            ramifica = False

        return [ramifica, SOLUCAO_OTIMA]

def branchAndBound(level, x, y, otimo , variablesAmount, solver, data):
    novasRes = [ -1 for _ in range(variablesAmount)]
    itens = [(a+1) for a in range(variablesAmount) ]
    p1 = Pack(level, x, y, otimo, variablesAmount, solver, data, novasRes, itens)
    SOLUCAO_OTIMA = -1

    queue = deque()
    queue.append(p1)

    id = 0
    while(len(queue) != 0):
        u = queue.popleft()

        [ramifica, SOLUCAO_OTIMA] = u.ramifica(SOLUCAO_OTIMA)
        if(ramifica == True):
            for i in range(len(u.itens)):
                v = Pack(u.level+1, x, y, otimo, variablesAmount, solver, u.data, u.novasRes, u.itens)
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
