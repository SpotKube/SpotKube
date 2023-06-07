import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_problem, get_algorithm, get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import Problem

from optimizer import helper
from collections import defaultdict

# Define the EC2 instances and their properties
# instances = {
#     "t2.micro": {"cpu": 1, "memory": 1, "cost": 0.01},
#     "t2.small": {"cpu": 1, "memory": 2, "cost": 0.02},
#     "t3.medium": {"cpu": 2, "memory": 4, "cost": 0.04},
#     # Add more instance types as needed
# }

# Define the microservice workloads and their properties
# workloads = {
#     "service1": {"cpu": 0.5, "memory": 0.5},
#     "service2": {"cpu": 1, "memory": 1},
#     "service3": {"cpu": 1.5, "memory": 2},
#     # Add more services as needed
# }


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
            nodes = defaultdict(dict)
            for j in range(len(x[i])):
                node_type = list(self.instances.keys())[j]
                num_nodes = int(x[i][j])
                total_instances[i] += num_nodes
                nodes[node_type]['cost'] = self.instances[node_type]["cost"] * num_nodes
            total_cost[i] = self.cost_func.cost(nodes)
            
            if not self.node_sufficient(self.flag, self.services, nodes, self.instances):
                total_cost[i],  total_instances[i] =  1e6, -1e6
        # Set the objectives (minimize cost, maximize number of instances)
        out["F"] = np.column_stack((-total_cost, total_instances))

def node_sufficient(flag, services, node_combination, instances):
    workload = helper.calculateResources(flag, services)
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())
    
    total_memory_nodes = 0
    total_cpu_nodes = 0
    
    for node in node_combination:
        total_memory_nodes += instances[node]['memory']
        total_cpu_nodes += instances[node]['cpu']
        
    if total_memory_nodes >= total_memory_pods and total_cpu_nodes >= total_cpu_pods:
        return True
    
    return False

def optimize(instances, flag, costFunc, services, allocated_nodes):
    r = len(helper.calculateResources(flag, services))
    problem = DeploymentProblem(cost_func = costFunc, node_sufficient = node_sufficient, flag = flag, services = services, instances = instances, r= r)

    # Define the algorithm and perform optimization
    algorithm = NSGA2(pop_size=50)
    termination = get_termination("n_gen", 50)
    res = minimize(problem,
                algorithm,
                termination,
                ("n_gen", 50),
                verbose=True)

    # Get the optimal solutions and objectives
    optimal_x = res.X
    optimal_f = res.F

    # Print the optimal solutions and objectives
    # print("Optimal Solutions:")
    # print("Optimal_x: ", optimal_x)
    # print("Optimal_f: ", optimal_f)
    # for i in range(len(optimal_x)):
    #     workload = list(workloads.keys())[i]
    #     num_instances = int(optimal_x[i])
    #     print(f"{workload}: {num_instances}")

    # print("Optimal Objectives:")
    # print(f"Total Cost: {-optimal_f[:, 0]}")
    # print(f"Number of Instances: {optimal_f[:, 1]}")
    
    nodes = defaultdict(dict)
    for i in range(len(optimal_x)):
            for j in range(len(optimal_x[i])):
                node_type = list(instances.keys())[j]
                num_nodes = int(optimal_x[i][j])
                nodes[f'solution_{i}'][node_type] = {"count": num_nodes}
            nodes[f'solution_{i}']['total_cost'] = -optimal_f[i][0]
    
    print(nodes)