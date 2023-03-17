import itertools
from bruteforce import helper

# Define the available node types and their prices
instances = helper.readJson('../.spotConfig.json') ### These file paths are relative to the main.py file in optimizer package

# Define the memory and CPU requirements of each service
service_requirements = {
    'Service 1': {'pods': 3,},
    'Service 2': {'pods': 5}
}

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])


def optimize():
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    # Define the total number of pods to deploy
    pod_requirements = helper.calculateResources(service_requirements)
    total_pods = len(pod_requirements)
    # Evaluate the cost function for each combination of nodes and select the optimal one
    optimal_cost = float('inf')
    optimal_nodes = None
    for nodes in (nodes for r in range(1, 2 * total_pods + 1) # r ranges from 1 to len(node_types) * total_pods + 1
                        for nodes in itertools.product(node_types.keys(), repeat=r)):
        # Calculate the total memory and CPU requirements of the nodes and pods
        total_memory_nodes = total_cpu_nodes = 0
        total_memory_pods = sum(pod['memory'] for pod in pod_requirements.values())
        total_cpu_pods = sum(pod['cpu'] for pod in pod_requirements.values())
        for node in nodes:
            total_memory_nodes += node_types[node]['memory']
            total_cpu_nodes += node_types[node]['cpu']

        # Check if the selected nodes can deploy all the pods
        if total_memory_nodes >= total_memory_pods and total_cpu_nodes >= total_cpu_pods:
            # Calculate the cost of the selected nodes
            cost = sum(node_types[node]['cost'] for node in nodes)
            if cost < optimal_cost:
                optimal_cost = cost
                optimal_nodes = nodes

    # Print the optimal solution
    if optimal_nodes is None:
        print("Unable to find a valid solution.")
    else:
        print("Optimal solution: {} (Cost: ${})".format(optimal_nodes, optimal_cost))
