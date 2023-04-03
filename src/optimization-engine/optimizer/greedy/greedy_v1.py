from optimizer import helper

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])

def optimize(instances, flag, costFunc=None):
    """
    Finds the optimal set of compute nodes for a workload given their hourly cost and resource availability
    using a greedy algorithm.

    Parameters:
    - instances (dict): a dictionary of resource availability for each compute node
    - flag (bool): to identify private vs spot services
    Returns:
    - optimal_nodes (list)): the set of compute nodes that minimizes the cost while satisfying the resource requirements
    """
    workload, max_pod_cpu, max_pod_memory = helper.calculateResources(flag)
    remaining_cpu = sum(pod['cpu'] for pod in workload.values())
    remaining_memory = sum(pod['memory'] for pod in workload.values())
    init_cpu = remaining_cpu
    init_memory = remaining_memory
    optimal_nodes = []

    sorted_nodes = dict(sorted(instances.items(), key=sort_node_types))
    
     # iterate over nodes and add them to the optimal set if they satisfy the resource requirements
    for node in sorted_nodes:
        pods_cpu = sorted_nodes[node]['cpu'] // init_cpu
        pods_memory = sorted_nodes[node]['memory'] // init_memory
        pods = min(pods_cpu, pods_memory)

        if pods > 0:
            optimal_nodes.append(node)
            remaining_cpu -= init_cpu * pods
            remaining_memory -= init_memory * pods

        if remaining_cpu == 0 and remaining_memory == 0:
            break

    return optimal_nodes