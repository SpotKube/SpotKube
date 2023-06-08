import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem, get_algorithm, get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import Problem

import matplotlib.pyplot as plt

from optimization_engine.optimizer.optimizerMain import helper

max_pod_cpu, max_pod_memory = helper.getPodDetails()

# Define a custom problem for deployment optimization
class DeploymentProblem(Problem):
    def __init__(self, cost_func, node_sufficient, workload, instances, r):
        super().__init__(n_var=len(instances),
                         n_obj=2,
                         n_constr=0,
                         elementwise_evaluation=True)

        self.r = r
        self.instances = instances
        self.xl = np.zeros(len(self.instances))
        self.xu = np.ones(len(self.instances)) * self.r
        self.cost_func = cost_func
        self.node_sufficient = node_sufficient
        self.workload = workload
        
    def _initialize(self):
        num_nodes = len(self.instances)
        self.x = np.full(num_nodes, 1)
        
    def _evaluate(self, x, out, *args, **kwargs):
    # Initialize variables for total cost and total instances
        total_cost = np.zeros(len(x))
        total_instances = np.zeros(len(x))

        for i in range(len(x)):
            nodes = []
            for j in range(len(x[i])):
                node_type = list(self.instances.keys())[j]
                num_nodes = int(round(x[i][j]))
                total_instances[i] += num_nodes
                nodes += [node_type] * num_nodes
            total_cost[i] = self.cost_func.cost(nodes)
            
            if not self.node_sufficient(self.workload, nodes, self.instances):
                total_cost[i],  total_instances[i] =  np.inf, -np.inf
            
        
        # Set the objectives (minimize cost, maximize number of instances)
        out["F"] = np.column_stack((total_cost, -total_instances))


def node_sufficient(workload, node_combination, instances):
    output = False
    total_pods = sum(service['pods'] for service in workload.values())
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())
    total_memory_nodes = 0
    total_cpu_nodes = 0
    
    for node in node_combination:
        total_memory_nodes += instances[node]['memory']
        total_cpu_nodes += instances[node]['cpu']
        
    memory_ration = round(total_memory_nodes / total_memory_pods, 2)
    cpu_ratio = round(total_cpu_nodes / total_cpu_pods, 2)
    if (1 <= memory_ration <= 2 and 1 <= cpu_ratio <= 2):
        remaining_pods = total_pods
        for node in node_combination:
            pod_mem = instances[node]['memory'] // max_pod_memory
            pod_cpu = instances[node]['cpu'] // max_pod_cpu
            remaining_pods -= min(pod_mem, pod_cpu)
            
            if (remaining_pods <= 0):
                output = True
                break
    
    return output

def plot_pareto(optimal_f):
    # Extract the cost and number of instances from the objectives
    total_cost = optimal_f[:, 0]
    total_instances = -optimal_f[:, 1]

    # Plot the Pareto optimal solutions
    plt.scatter(total_instances, total_cost)
    plt.ylabel('Total Cost') # minimize
    plt.xlabel('Number of Instances') # maximize
    plt.title('Pareto Optimal Solutions')
    plt.grid(True)
    plt.show()
    
def display_optimal_solution(optimal_x, optimal_f, instances):
    for i in range(len(optimal_x)):
        node_combination = []
        for j in range(len(optimal_x[i])):
            if int(round(optimal_x[i][j])) >= 1:
                node_type = list(instances.keys())[j]
                num_nodes = int(round(optimal_x[i][j]))
                node_combination.extend([node_type] * num_nodes)
        cost = optimal_f[i][0]  # Extract the cost from the objective values

        print("Node Combination:", node_combination)
        print("Total Cost:", cost)

def choose_node_combination(optimal_x, optimal_f, instances, i):
    node_combination = []
    for j in range(len(optimal_x[i])):
        if int(round(optimal_x[i][j])) >= 1:
            node_type = list(instances.keys())[j]
            num_nodes = int(round(optimal_x[i][j]))
            node_combination.extend([node_type] * num_nodes)
    cost = optimal_f[i][0]
    print(f'Optimal node comb @ {i}', node_combination)
    print(f'Optimal Cost @ {i}: ', cost)
    return node_combination

def sort_nodes(optimal_x, optimal_f):
    sorted_indices = np.argsort(optimal_f[:, 0])  # Sort based on the first objective (cost)
    sorted_optimal_f = optimal_f[sorted_indices]
    sorted_optimal_x = optimal_x[sorted_indices]
    return sorted_optimal_x, sorted_optimal_f

def optimize(instances, flag, costFunc, services, allocated_nodes):
    workload = helper.calculateResources(flag, services)
    if (len(workload) == 0):
        return []
    r = len(workload) * 2
    if (flag):
        r = helper.getPrivateNodeCount()
    problem = DeploymentProblem(cost_func = costFunc, node_sufficient = node_sufficient, workload = workload, instances = instances, r= r)

    # Define the algorithm and perform optimization
    algorithm = NSGA2(pop_size=50)
    termination = get_termination("n_gen", 50)
    res = minimize(problem,
                algorithm,
                termination,
                ("n_gen", 100),
                verbose=True)

    # Get the optimal solutions and objectives
    optimal_x = res.X
    optimal_f = res.F
    
    print("Wokloads: ", workload)
    optimal_x, optimal_f = sort_nodes(optimal_x, optimal_f)
    i = len(optimal_x) // 2
    node_comb = choose_node_combination(optimal_x, optimal_f,instances, i)
    choose_node_combination(optimal_x, optimal_f,instances, 0)
    choose_node_combination(optimal_x, optimal_f,instances, -1)
    return node_comb
   