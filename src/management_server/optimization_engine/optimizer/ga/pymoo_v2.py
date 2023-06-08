import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem, get_algorithm, get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import Problem

import matplotlib.pyplot as plt

from optimizer import helper


# Define a custom problem for deployment optimization
class DeploymentProblem(Problem):
    def __init__(self, cost_func, node_sufficient, flag, services, instances, r):
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
        self.flag = flag
        self.services = services
        
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
            
            if not self.node_sufficient(self.flag, self.services, nodes, self.instances):
                total_cost[i],  total_instances[i] =  np.inf, -np.inf
            
            # print(nodes)
            # print(total_cost[i],  total_instances[i])
        # Set the objectives (minimize cost, maximize number of instances)
        out["F"] = np.column_stack((total_cost, -total_instances))


def node_sufficient(flag, services, node_combination, instances):
    output = False
    workload = helper.calculateResources(flag, services)
    max_pod_cpu, max_pod_memory = helper.getPodDetails()
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
    if (1 <= memory_ration <= 4 and 1 <= cpu_ratio <= 4):
        remaining_pods = total_pods
        for node in node_combination:
            pod_mem = instances[node]['memory'] // max_pod_memory
            pod_cpu = instances[node]['cpu'] // max_pod_cpu
            remaining_pods -= min(pod_mem, pod_cpu)
            
            if (remaining_pods <= 0):
                output = True
                break
    
    # print("node sufficient output: ",output)
    return output

def plot_pareto(optimal_f):
    # Extract the cost and number of instances from the objectives
    total_cost = optimal_f[:, 0]
    total_instances = -optimal_f[:, 1]

    # Plot the Pareto optimal solutions
    plt.scatter(total_cost, total_instances)
    plt.xlabel('Total Cost')
    plt.ylabel('Number of Instances')
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
        
def optimize(instances, flag, costFunc, services, allocated_nodes):
    workload = helper.calculateResources(flag, services)
    r = len(workload)
    problem = DeploymentProblem(cost_func = costFunc, node_sufficient = node_sufficient, flag = flag, services = services, instances = instances, r= r)

    # Define the algorithm and perform optimization
    algorithm = NSGA2(pop_size=100)
    termination = get_termination("n_gen", 100)
    res = minimize(problem,
                algorithm,
                termination,
                ("n_gen", 100),
                verbose=True)

    # Get the optimal solutions and objectives
    optimal_x = res.X
    optimal_f = res.F
    
    # print("Optimal_x: ", optimal_x)
    # print("Optimal_f: ", optimal_f)

    # Print the optimal solutions and objectives
    # print("Optimal Solutions:")
    # for i in range(len(optimal_x)):
    #     workload = list(workloads.keys())[i]
    #     num_instances = int(optimal_x[i])
    #     print(f"{workload}: {num_instances}")

    
    
    
    
    # best_solution_index = 0
    # for i in range(1, len(optimal_x)):
    #     if optimal_f[i][0] < optimal_f[best_solution_index][0] and -optimal_f[i][1] > -optimal_f[best_solution_index][1]:
    #         best_solution_index = i

    # # Store the selected node combination and total cost of the best solution
    # best_solution_x = optimal_x[best_solution_index]
    # best_solution_total_cost = optimal_f[best_solution_index][0]
    # best_solution_total_count = -optimal_f[best_solution_index][1]


    # # Print or return the best solution
    # print("Best Solution:")
    # print("Optimal_x: ", best_solution_x)
    # print("Total Cost: ", best_solution_total_cost)
    # print("Total Count: ", best_solution_total_count)
    
    print("Wokloads: ", workload)
    display_optimal_solution(optimal_x, optimal_f, instances)
    plot_pareto(optimal_f)
   