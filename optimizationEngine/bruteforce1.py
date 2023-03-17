import itertools

# Define the available node types and their prices
node_types = {
    't3.medium': {'cpu': 2, 'memory': 4, 'cost': 0.01},
    'm6g.medium': {'cpu': 1, 'memory': 4, 'cost': 0.01},
    'c6a.large': {'cpu': 2, 'memory': 4, 'cost': 0.02},
    't4g.large': {'cpu': 2, 'memory': 8, 'cost': 0.02},
    'c6g.xlarge': {'cpu': 4, 'memory': 8, 'cost': 0.06},
    't2.small': {'cpu': 1, 'memory': 2, 'cost': 0.006}
}

# Define the memory and CPU requirements of each pod
pod_requirements = {
    'Service 1': {'memory': 3, 'cpu': 2},
    'Service 2': {'memory': 5, 'cpu': 2},
}

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])
node_types = dict(sorted(node_types.items(), key=sort_node_types))

# Define the total number of pods to deploy
total_pods = len(pod_requirements)

# Generate all possible combinations of nodes with repetition based on the pod requirements
# node_combinations = (nodes for r in range(1, len(node_types) * total_pods + 1) # r ranges from 1 to len(node_types) * total_pods + 1
#                     for nodes in itertools.product(node_types.keys(), repeat=r))

# Evaluate the cost function for each combination of nodes and select the optimal one
optimal_cost = float('inf')
optimal_nodes = None
for nodes in (nodes for r in range(1, 2 * total_pods + 1) # r ranges from 1 to len(node_types) * total_pods + 1
                    for nodes in itertools.product(node_types.keys(), repeat=r)):
    # Calculate the total memory and CPU requirements of the nodes and pods
    print(nodes)
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
