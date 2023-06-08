import random
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem, get_termination
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.optimize import minimize

from optimizer import helper

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])

class NodeCombinationProblem:
    def __init__(self, node_types, max_r, total_memory_pods, total_cpu_pods):
        self.node_types = node_types
        self.max_r = max_r
        self.total_memory_pods = total_memory_pods
        self.total_cpu_pods = total_cpu_pods
        # Set the number of decision variables
        self.n_var = len(node_types)
        self.xl = np.zeros(self.n_var, dtype=bool)
        
    def evaluate(self, X, out, *args, **kwargs):
        node_counts = np.count_nonzero(X, axis=1)
        total_costs = np.sum(X * np.array([node_type['cost'] for node_type in self.node_types]), axis=1)
        
        out["F"] = np.column_stack((-node_counts, total_costs))
        
    def crossover(self, X, *args, **kwargs):
        _, n_genes = X.shape
        n_children = len(X) // 2
        
        offspring = np.zeros((n_children, n_genes), dtype=bool)
        
        for i in range(n_children):
            parent1 = X[2*i]
            parent2 = X[2*i + 1]
            
            # Perform crossover between parent1 and parent2 (e.g., single-point crossover)
            crossover_point = random.randint(1, n_genes - 1)
            offspring[i, :crossover_point] = parent1[:crossover_point]
            offspring[i, crossover_point:] = parent2[crossover_point:]
        
        return offspring
    
    def mutation(self, X, *args, **kwargs):
        n_individuals, n_genes = X.shape
        
        # Perform mutation on the individuals (e.g., flip a bit)
        for i in range(n_individuals):
            for j in range(n_genes):
                if random.random() < 0.01:
                    X[i, j] = not X[i, j]
        
        return X

def nsga_optimize(instances, flag, costFunc, services):
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    workload = helper.calculateResources(flag, services)
    total_services = len(workload)
    max_pod_cpu, max_pod_memory = helper.getPodDetails()
     
    if flag:
        private_node_count = helper.getPrivateNodeCount()
    max_r = 2 * total_services
    if flag and max_r > private_node_count:
        max_r = private_node_count
    total_pods = sum(service['pods'] for service in workload.values())
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())
    
    problem = NodeCombinationProblem(node_types, max_r, total_memory_pods, total_cpu_pods)
    
    # Define the optimization problem
    algorithm = NSGA2(
        pop_size=100,
        crossover=CustomCrossover(),
        mutation=CustomMutation(),
        eliminate_duplicates=True
    )
    
    termination = get_termination("n_gen", 100)
    
    res = minimize(problem, algorithm, termination=termination)
    
    return res.X, res.F

# Custom crossover operator
class CustomCrossover(Crossover):
    def __init__(self):
        super().__init__(2, 2)
    
    def _do(self, problem, X, **kwargs):
        return problem.crossover(X)

# Custom mutation operator
class CustomMutation(Mutation):
    def __init__(self):
        super().__init__()
    
    def _do(self, problem, X, **kwargs):
        return problem.mutation(X)



def optimize(instances, flag, costFunc, services, allocated_nodes):
    nodes, objectives = nsga_optimize(instances, flag, costFunc, services)
    for i in range(len(nodes)):
        print(f"Node Count: {np.count_nonzero(nodes[i])}, Total Cost: {objectives[i][1]}, Nodes: {nodes[i]}")
