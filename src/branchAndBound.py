
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

    def optimalSolution(self):

        # Função objetiva. Minimza o numero de caminhões utilizados.
        i = 0
        while(i < len(self.novasRes) and self.novasRes[i] != -1):
            print("AAAAAAAAAAAAAA: %d e %d" % (self.level, self.novasRes[i]))
            self.solver.Add(self.x[self.novasRes[i], self.level] == 1)
            i += 1

        self.solver.Minimize(self.solver.Sum([self.y[j] for j in self.data['trucks']]))

        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            num_bins = 0.
            for j in self.data['trucks']:
                # print(f"y[{j}]",y[j].solution_value())
                if self.y[j].solution_value() >= 0:
                    bin_items = []
                    bin_weight = 0
                    for i in self.data['items']:
                        # print(f"x[{i}, {j}]",x[i,j].solution_value())

                        bin_items.append(i)
                        bin_weight += self.data['weights'][i]
                    print()
                    if bin_weight >= 0:
                        num_bins += 1
                        print('Bin number', j)
                        print('  Items packed:', bin_items)
                        print('  Total weight:', bin_weight)
                        print()
            print()
            print('Number of bins used:', num_bins)
            print('Time = ', self.solver.WallTime(), ' milliseconds')
        else:
            print('The problem does not have an optimal solution.\n')

def verificaRamificacao():

    return

def branchAndBound(level, x, y, otimo , variablesAmount, solver, data):
    p1 = Pack(level, x, y, otimo, variablesAmount, solver, data)

    queue = deque()
    queue.append(p1)


    while(len(queue) != 0):
        u = queue.popleft()
        print(u.maxLevel)

        if(u.level == u.maxLevel):
            continue

        for i in range(len(u.itens)):
            v = Pack(level, x, y, otimo, variablesAmount, solver, data)
            







    return
