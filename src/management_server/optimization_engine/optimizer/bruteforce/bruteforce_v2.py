import itertools
from optimizer import helper

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])


def optimize(instances, flag, costFunc, services):
    """
    Finds the optimal set of compute nodes for a workload given their hourly cost and resource availability
    using a bruteforce algorithm.

    Parameters:
    - instances (dict): a dictionary of resource availability for each compute node
    - flag (bool): to identify private vs spot services
    - costFunc (func): Function to calculate the cost of each node combination
    
    Method:
    - Calculating the optimal cost for deploying all the pods in a set of nodes
    Pods are mapped into the nodes rather than mapping actual cpu and memory usage
    
    Returns:
    - optimal_nodes (list): the set of compute nodes that minimizes the cost while satisfying the resource requirements
    """
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
    # Evaluate the cost function for each combination of nodes and select the optimal one
    optimal_cost = float('inf')
    optimal_nodes = None
    for nodes in (nodes for r in range(1, max_r + 1) # r ranges from 1 to len(node_types) * total_services + 1
                        for nodes in itertools.product(node_types.keys(), repeat=r)):
        # sort the set of nodes based on the cost
        nodes = sorted(nodes, key=lambda node: node_types[node]['cost'])
        # Calculate the total memory and CPU requirements of the nodes
        total_memory_nodes = 0
        total_cpu_nodes = 0
        for node in nodes:
            total_memory_nodes += node_types[node]['memory']
            total_cpu_nodes += node_types[node]['cpu']

        # Check if the selected nodes can deploy all the pods
        if total_memory_nodes >= total_memory_pods and total_cpu_nodes >= total_cpu_pods:
            # Calculate the cost of the selected nodes
            cost = costFunc.cost(nodes)
            if cost < optimal_cost:
                remaining_pods = total_pods
                for node in nodes:
                    pod_mem = node_types[node]['memory'] // max_pod_memory
                    pod_cpu = node_types[node]['cpu'] // max_pod_cpu
                    remaining_pods -= min(pod_mem, pod_cpu)
                    
                if (remaining_pods <= 0):
                    optimal_cost = cost
                    optimal_nodes = nodes

    # Print the optimal solution
    print(f"Services need to be deployed {workload}")
    if optimal_nodes is None:
        print("Unable to find a valid solution.")
    else:
        print("Optimal solution: {} (Cost: ${})".format(optimal_nodes, optimal_cost))

    return optimal_nodes