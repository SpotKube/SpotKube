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
    - Services: This list contains services and pod count -> [{'name': 'service3', 'pods': 6}, {'name': 'service4', 'pods': 6}]
    
    Method:
    - Considered mapping the total required resources with the node resources.
    But this method won't be a idle, since we are deploying services as pods
    we need to consider pods as it is. This will be addressed in v2
    
    Returns:
    - optimal_nodes (list)): the set of compute nodes that minimizes the cost while satisfying the resource requirements
    """
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    workload = helper.calculateResources(flag, services)
    total_services = len(workload)
    max_r = 2 * total_services
    if (flag):
        private_node_count = helper.getPrivateNodeCount()
    if (flag and max_r > private_node_count):
        max_r = private_node_count
    # Evaluate the cost function for each combination of nodes and select the optimal one
    optimal_cost = float('inf')
    optimal_nodes = None
    for nodes in (nodes for r in range(1, max_r + 1) # r ranges from 1 to len(node_types) * total_pods + 1
                        for nodes in itertools.product(node_types.keys(), repeat=r)):
        # Calculate the total memory and CPU requirements of the nodes and pods
        total_memory_nodes = total_cpu_nodes = 0
        total_memory_pods = sum(pod['memory'] for pod in workload.values())
        total_cpu_pods = sum(pod['cpu'] for pod in workload.values())
        for node in nodes:
            total_memory_nodes += node_types[node]['memory']
            total_cpu_nodes += node_types[node]['cpu']

        # Check if the selected nodes can deploy all the pods
        if total_memory_nodes >= total_memory_pods and total_cpu_nodes >= total_cpu_pods:
            # Calculate the cost of the selected nodes
            cost = costFunc.cost(nodes)
            if cost < optimal_cost:
                optimal_cost = cost
                optimal_nodes = nodes

    # Print the optimal solution
    print(f"Services need to be deployed {workload}")
    if optimal_nodes is None:
        print("Unable to find a valid solution.")
    else:
        print("Optimal solution: {} (Cost: ${})".format(optimal_nodes, optimal_cost))

    return optimal_nodes