import heapq
from optimization_engine.optimizer.optimizerMain import helper

# sort node types based on the cost
def sort_node_types(item):
    return float(item[1]['cost'])

def optimize(instances, flag, costFunc, services, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns):
    """
    Finds the optimal set of compute nodes for a workload given their hourly cost and resource availability
    using a greedy algorithm.

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
    for node in instances.keys():
        instances[node]['cpu'] = instances[node]['cpu'] - round(cpu_usage_of_ds_in_other_ns*0.001, 2)
    
    node_types = dict(sorted(instances.items(), key=sort_node_types))
    workload = helper.calculateResources(flag, services)
    max_pod_cpu, max_pod_memory = helper.getPodDetails()
    
    private_node_count = helper.getPrivateNodeCount()
    total_pods = sum(service['pods'] for service in workload.values())
    total_memory_pods = sum(service['memory'] for service in workload.values())
    total_cpu_pods = sum(service['cpu'] for service in workload.values())
    
    # Initialize a heap to store the available nodes, sorted by cost
    node_heap = [(node_types[node]['cost'], node) for node in node_types.keys()]
    heapq.heapify(node_heap)
    
    # Initialize the set of selected nodes and remaining pods
    selected_nodes = []
    remaining_pods = total_pods
    
    # Select nodes until all pods are assigned or there are no more available nodes
    i = 0
    while remaining_pods > 0 and len(node_heap) > 0:   
        if (flag and len(selected_nodes) > private_node_count):
            # No nodes available for private cluster to allocate
            break
        # Select the most cost-effective node with sufficient resources to satisfy the resource requirements of the pod
        _, node = heapq.heappop(node_heap)
        if node_types[node]['memory'] >= max_pod_memory and node_types[node]['cpu'] >= max_pod_cpu:
            # Calculate the number of pods that can be assigned to the node
            node_mem = node_types[node]['memory']
            node_cpu = node_types[node]['cpu']
            if (i == 0):
                node_cpu -= round(cpu_usage_of_pods_in_other_ns*0.001, 2)
            pod_mem = node_mem // max_pod_memory
            pod_cpu = node_cpu // max_pod_cpu
            pods = min(pod_mem, pod_cpu)
            
            remaining_pods -= pods
            total_memory_pods -= pods * max_pod_memory
            total_cpu_pods -= pods * max_pod_cpu
        
            cost = round(node_types[node]['cost'] + costFunc.cost(selected_nodes), 3)
            heapq.heappush(node_heap, (cost, node))
            print(node_heap)
            
            # Assign the pods to the node
            selected_nodes.append(node)
            i += 1
            
    # Print the optimal solution
    print(f"Services need to be deployed {workload}")
    if remaining_pods > 0:
        print("Unable to find a valid solution.")
        optimal_nodes = None
    else:
        optimal_cost = costFunc.cost(selected_nodes)
        optimal_nodes = list(selected_nodes)
        print(f"Optimal solution: {optimal_nodes} Cost: ${optimal_cost}")
