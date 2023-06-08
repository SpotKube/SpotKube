import random
from deap import base, creator, tools, algorithms

# Define the problem-specific functions and parameters
# ----------------------------------------------

# Define the creator for the optimization problem
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))  # Minimize cost and maximize node count
creator.create("Individual", list, fitness=creator.FitnessMin)

# Define the range and properties of the problem variables
# (e.g., node types, cost function, workload)
node_types = ['Node1', 'Node2', 'Node3']  # Example list of node types
node_costs = {'Node1': 10, 'Node2': 15, 'Node3': 20}  # Example dictionary of node costs
node_capacities = {'Node1': {'RAM': 8, 'CPU': 4},
                   'Node2': {'RAM': 16, 'CPU': 8},
                   'Node3': {'RAM': 32, 'CPU': 16}}  # Example dictionary of node capacities
workload = {'RAM': 24, 'CPU': 12}  # Example workload (RAM and CPU usage)

# Define the evaluation function
def evaluate(individual):
    total_cost = 0
    node_count = 0
    ram_sum = 0
    cpu_sum = 0

    for node_type in individual:
        if node_type not in node_costs:
            return float('inf'), 0  # Return a high cost and zero node count for invalid solutions
        total_cost += node_costs[node_type]
        node_count += 1
        ram_sum += node_capacities[node_type]['RAM']
        cpu_sum += node_capacities[node_type]['CPU']

    ram_constraint = ram_sum - workload['RAM']
    cpu_constraint = cpu_sum - workload['CPU']
    
    # Check if RAM and CPU constraints are satisfied
    if ram_constraint <= 0 and cpu_constraint <= 0:
        return total_cost, node_count
    else:
        return float('inf'), 0  # Return a high cost and zero node count for infeasible solutions

def optimize(instances, flag, costFunc, services, allocated_nodes):
    # Initialize the toolbox
    toolbox = base.Toolbox()
    toolbox.register("node_type", random.choice, node_types)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.node_type, n=5)  # Set the number of nodes here
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(node_types)-1, indpb=0.2)
        
    # Custom selection operator for NSGA-II
    def custom_selection(population, k):
        fronts = tools.sortNondominated(population, k=k, first_front_only=True)
        selected = []

        for front in fronts:
            if len(selected) + len(front) <= k:
                selected.extend(front)
            else:
                crowding_dist = calculate_crowding_distance(front)
                sorted_front = [x for _, x in sorted(zip(crowding_dist, front), reverse=True)]
                selected.extend(sorted_front[:k - len(selected)])
                break

        return selected
    
    def calculate_crowding_distance(front):
        num_objectives = len(front[0].fitness.values)
        distances = [0.0] * len(front)

        for i in range(num_objectives):
            sorted_front = sorted(front, key=lambda ind: ind.fitness.values[i])
            distances[0] = float('inf')
            distances[-1] = float('inf')

            if sorted_front[-1].fitness.values[i] == sorted_front[0].fitness.values[i]:
                continue

            for j in range(1, len(front) - 1):
                distances[j] += (sorted_front[j+1].fitness.values[i] - sorted_front[j-1].fitness.values[i]) / (
                        sorted_front[-1].fitness.values[i] - sorted_front[0].fitness.values[i])

        return distances


    toolbox.register("select", custom_selection)

    # Set the algorithm parameters
    population_size = 50
    generations = 100
    crossover_probability = 0.9
    mutation_probability = 0.1

    # Run the optimization
    random.seed(42)

    population = toolbox.population(n=population_size)

    for generation in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=crossover_probability, mutpb=mutation_probability)
        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit
        population = toolbox.select(offspring + population, k=population_size)

        # Gather all the unique fitness values in the population
        unique_fitnesses = set(ind.fitness.values for ind in population)

        # If the number of unique fitness values equals the population size,
        # it means all solutions are non-dominated and we can stop the optimization
        if len(unique_fitnesses) == population_size:
            break

    # Get the Pareto front solutions
    pareto_front = tools.selBest(population, k=population_size)

    # Print the Pareto front solutions
    for solution in pareto_front:
        print("Solution: ", solution)
        print("Cost: ", solution.fitness.values[0])
        print("Node Count: ", solution.fitness.values[1])
        print("-----------------------")
