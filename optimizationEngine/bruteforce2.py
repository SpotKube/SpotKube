import itertools

# Define the available node types and their prices
node_types = {
    't2.small': {'cpu': 1, 'memory': 2, 'cost': 0.006},
    't3.medium': {'cpu': 2, 'memory': 4, 'cost': 0.01},
    'm6g.medium': {'cpu': 1, 'memory': 4, 'cost': 0.01},
    'c6a.large': {'cpu': 2, 'memory': 4, 'cost': 0.02},
    't4g.large': {'cpu': 2, 'memory': 8, 'cost': 0.02},
    'c6g.xlarge': {'cpu': 4, 'memory': 8, 'cost': 0.06},
}


# Define the memory and CPU requirements of each pod
pod_requirements = {
    'Service 1': {
        'memory': 2,
        'cpu': 1,
    },
    'Service 2': {
        'memory': 2,
        'cpu': 1,
    },
    # Add more pods here if needed
}

# Define the total number of pods to deploy
total_pods = len(pod_requirements)

# Generate all possible combinations of nodes with repetition based on the pod requirements
node_combinations = []
for r in range(1, 3): # r ranges from 1 to len(node_types) * total_pods + 1
    for nodes in itertools.product(node_types.keys(), repeat=r):
        # Check if the selected nodes can deploy all the pods
        total_memory = sum(node_types[node]['memory'] for node in nodes)
        total_cpu = sum(node_types[node]['cpu'] for node in nodes)
        if total_memory >= sum(pod['memory'] for pod in pod_requirements.values()) \
                and total_cpu >= sum(pod['cpu'] for pod in pod_requirements.values()):
            node_combinations.append(nodes)

# Evaluate the cost function for each combination of nodes and select the optimal one
optimal_cost = float('inf')
optimal_nodes = None
for nodes in node_combinations:
    # Calculate the total memory and CPU capacity of the selected nodes
    total_memory = sum(node_types[node]['memory'] for node in nodes)
    total_cpu = sum(node_types[node]['cpu'] for node in nodes)

    # Check if the selected nodes can deploy all the pods
    if total_memory >= sum(pod['memory'] for pod in pod_requirements.values()) \
            and total_cpu >= sum(pod['cpu'] for pod in pod_requirements.values()):
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
