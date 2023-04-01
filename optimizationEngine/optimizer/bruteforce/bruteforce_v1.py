import itertools
from optimizer import helper

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])


def optimize(instances, costFunc, flag):
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    # Define the total number of pods to deploy
    pod_requirements = helper.calculateResources(flag)
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
            cost = costFunc.cost(nodes)
            if cost < optimal_cost:
                optimal_cost = cost
                optimal_nodes = nodes

    # Print the optimal solution
    print(f"Services need to be deployed {pod_requirements}")
    if optimal_nodes is None:
        print("Unable to find a valid solution.")
    else:
        print("Optimal solution: {} (Cost: ${})".format(optimal_nodes, optimal_cost))

    return optimal_nodes