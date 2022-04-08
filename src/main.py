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
    dictInput = {
        "firstLine": [],
        "weights": [],
        "ordered_pairs": [],
    }

    leInputs(dictInput)
    # print(dictInput)

    data["weights"] = dictInput["weights"]
    data["items"] = list(range(len(dictInput["weights"])))
    data["bins"] = data["items"]
    data["ordered_pairs"] = dictInput["ordered_pairs"]
    data["bin_capacity"] = 10

    return data;


def main():
    data = create_model()
    print(data, "\n\n")

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver('binPacking',
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.NumVar(0.0, 1.0, 'x_%i_%i' % (i, j))

    # y[j] = 1 if bin j is used.
    y = {}
    for j in data['bins']:
        y[j] = solver.NumVar(0.0, 1.0, 'y[%i]' % j)

    # Constraints
    # Each item must be in exactly one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items']) - (data["bin_capacity"]*y[j]) == 0
        )


    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum([y[j] for j in data['bins']]))

    # status = solver.Solve()
    solver.Solve()
    print("Object value = ", solver.Objective().Value())
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    # if status == pywraplp.Solver.OPTIMAL:
    #     num_bins = 0.
    #     for j in data['bins']:
    #         bin_items = []
    #         bin_weight = 0
    #         for i in data['items']:
    #             if x[i, j].solution_value() > 0:
    #                 bin_items.append(i)
    #                 bin_weight += data['weights'][i]
    #         if bin_weight > 0:
    #             num_bins += 1
    #             print('Bin number', j)
    #             print('  Items packed:', bin_items)
    #             print('  Total weight:', bin_weight)
    #             print()
    #     print()
    #     print('Number of bins used:', num_bins)
    #     print('Time = ', solver.WallTime(), ' milliseconds')
    # else:
    #     print('The problem does not have an optimal solution.')

if __name__ == "__main__":
    main()
