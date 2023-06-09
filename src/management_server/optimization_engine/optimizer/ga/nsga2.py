import random
from optimizer import helper

def sort_node_types(item):
    return float(item[1]['cost'])

def evaluate_objective_functions(nodes):
    # Calculate the node count
    node_count = len(nodes)
    
    # Calculate the total cost
    total_cost = sum(node_types[node]['cost'] for node in nodes)
    
    return node_count, total_cost

def dominates(solution1, solution2):
    # Check if solution1 dominates solution2
    node_count1, cost1 = solution1
    node_count2, cost2 = solution2
    
    return node_count1 >= node_count2 and cost1 <= cost2

def non_dominated_sort(population):
    # Perform non-dominated sorting on the population
    fronts = [[]]
    domination_count = {solution: 0 for solution in population}
    dominated_solutions = {solution: [] for solution in population}
    
    for i, solution1 in enumerate(population):
        for j, solution2 in enumerate(population[i+1:], start=i+1):
            if dominates(solution1, solution2):
                dominated_solutions[solution1].append(solution2)
                domination_count[solution2] += 1
            elif dominates(solution2, solution1):
                dominated_solutions[solution2].append(solution1)
                domination_count[solution1] += 1
        
        if domination_count[solution1] == 0:
            fronts[0].append(solution1)
    
    index = 0
    while len(fronts[index]) > 0:
        next_front = []
        for solution1 in fronts[index]:
            for solution2 in dominated_solutions[solution1]:
                domination_count[solution2] -= 1
                if domination_count[solution2] == 0:
                    next_front.append(solution2)
        index += 1
        fronts.append(next_front)
    
    return fronts

def crowding_distance_sort(front):
    # Perform crowding distance sorting within a front
    num_solutions = len(front)
    
    distances = {solution: 0 for solution in front}
    
    objectives = list(zip(*front))
    num_objectives = len(objectives)
    
    for objective in objectives:
        sorted_indices = sorted(range(num_solutions), key=lambda i: objective[i])
        
        distances[front[sorted_indices[0]]] = float('inf')
        distances[front[sorted_indices[-1]]] = float('inf')
        
        for i in range(1, num_solutions-1):
            distances[front[sorted_indices[i]]] += objective[sorted_indices[i+1]] - objective[sorted_indices[i-1]]
    
    return sorted(front, key=lambda solution: distances[solution], reverse=True)

def selection(population):
    # Perform selection using tournament selection
    tournament_size = 2
    selected = []
    
    while len(selected) < len(population):
        tournament = random.sample(population, tournament_size)
        best_solution = max(tournament, key=lambda solution: crowding_distance[solution])
        selected.append(best_solution)
    
    return selected

def crossover(parent1, parent2):
    # Perform crossover between two parents
    # Implement your crossover operator here
    # Return the resulting offspring

def mutation(individual):
    # Perform mutation on an individual
    # Implement your mutation operator here
    # Return the resulting mutated individual

def nsga2_optimize(instances, flag, population_size, max_generations):
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    workload = helper.calculateResources(flag, services)
    total_services = len(workload)
    max_pod_cpu, max_pod_memory = helper.getPodDetails()
    
    if (flag):
        private_node_count = helper.getPrivateNodeCount()
    max_r = 2 * total_services
    if (flag and max_r > private_node_count):
        max_r = private_node_count
    total_pods = sum(service['pods'] for service in workload.values())
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())
    
    population = []
    
    # Initialize the population randomly
    for _ in range(population_size):
        nodes = random.choices(list(node_types.keys()), k=random.randint(1, max_r))
        population.append(nodes)
    
    # Main loop
    for _ in range(max_generations):
        # Evaluate objective functions for the population
        evaluated_population = []
        for nodes in population:
            node_count, cost = evaluate_objective_functions(nodes)
            evaluated_population.append((node_count, cost))
        
        # Perform non-dominated sorting
        fronts = non_dominated_sort(evaluated_population)
        
        new_population = []
        front_index = 0
        while len(new_population) + len(fronts[front_index]) <= population_size:
            new_population.extend(fronts[front_index])
            front_index += 1
        
        remaining_population = crowding_distance_sort(fronts[front_index])
        new_population.extend(remaining_population[:population_size - len(new_population)])
        
        population = new_population
        
        # Create offspring through crossover and mutation
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            child = mutation(child)
            offspring.append(child)
        
        population.extend(offspring)
    
    # Final non-dominated sorting
    evaluated_population = []
    for nodes in population:
        node_count, cost = evaluate_objective_functions(nodes)
        evaluated_population.append((node_count, cost))
    
    fronts = non_dominated_sort(evaluated_population)
    
    return fronts[0]
