import heapq
from optimizer import helper

def optimize(instances, flag, costFunc):
    """
    Finds the optimal set of compute nodes for a workload given their hourly cost and resource availability
    using a greedy algorithm.

    Parameters:
    - instances (dict): a dictionary of resource availability for each compute node
    - flag (bool): to identify private vs spot services
    - costFunc (func): Function to calculate the cost of each node combination
    
    Method:
    - Calculate the optimal cost for deploying all the pods in a set of nodes
    - Pods are mapped into the nodes rather than mapping actual cpu and memory usage
    
    Returns:
    - optimal_nodes (list): the set of compute nodes that minimizes the cost while satisfying the resource requirements
    """
    node_types = dict(sorted(instances.items(), key=lambda item: float(item[1]['cost'])))
    workload, max_pod_cpu, max_pod_memory = helper.calculateResources(flag)
    
    private_node_count = helper.getPrivateNodeCount()
    total_pods = sum(service['pods'] for service in workload.values())
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())

    # Initialize a priority queue of nodes based on their cost
    node_queue = [(node_types[node]['cost'], node) for node in node_types.keys()]
    heapq.heapify(node_queue)

    # Assign pods to the node with the lowest cost until its resource limits are reached
    nodes = []
    while total_pods > 0:
        if (flag and len(nodes) > private_node_count):
            # No nodes available for private cluster to allocate
            break
        if not node_queue:
            # No nodes left to assign pods to
            break
        _, node = heapq.heappop(node_queue)
        if node_types[node]['memory'] >= max_pod_memory and node_types[node]['cpu'] >= max_pod_cpu:
            # Node can fit at least one pod
            nodes.append(node)
            total_memory_pods -= node_types[node]['memory']
            total_cpu_pods -= node_types[node]['cpu']
            total_pods -= 1
        else:
            # Node can't fit any more pods, remove from consideration
            node_types.pop(node)

        # Update the priority queue with the remaining nodes
        node_queue = [(node_types[node]['cost'], node) for node in node_types.keys()]
        heapq.heapify(node_queue)

    # Calculate the cost of the selected nodes
    optimal_cost = costFunc.cost(nodes) if nodes else float('inf')

    # Print the optimal solution
    print(f"Services need to be deployed {workload}")
    if not nodes:
        print("Unable to find a valid solution.")
    else:
        print("Optimal solution: {} (Cost: ${})".format(nodes, optimal_cost))

    return nodes