import math

# Instance types and their properties (vCPUs, memory, and hourly cost)
instances = {
    't2.small': {'vcpus': 1, 'memory': 2, 'cost': 0.006},
    't3.medium': {'vcpus': 2, 'memory': 4, 'cost': 0.01},
    'm6g.medium': {'vcpus': 1, 'memory': 4, 'cost': 0.01},
    'c6a.large': {'vcpus': 2, 'memory': 4, 'cost': 0.02},
    't4g.large': {'vcpus': 2, 'memory': 8, 'cost': 0.02},
    'c6g.xlarge': {'vcpus': 4, 'memory': 8, 'cost': 0.06},
}

# Pod requirements (vCPUs and memory)
pod_reqs = {'vcpus': 0.2, 'memory': 0.4}

# Recursive function to find the optimal combination of instances
def find_optimal_instance_combination(resources_required, instance_types, instance_counts, cost_so_far):
    # Base case: if all instance types have been considered, return the current cost
    if not instance_types:
        return cost_so_far
    
    # Try all possible counts for the current instance type
    current_instance_type = instance_types[0]
    current_instance_count = instance_counts.get(current_instance_type, 0)
    min_cost = math.inf
    for i in range(resources_required['vcpus'] // instances[current_instance_type]['vcpus'] + 1):
        for j in range(resources_required['memory'] // instances[current_instance_type]['memory'] + 1):
            # Calculate the remaining resources required
            remaining_vcpus = resources_required['vcpus'] - i * instances[current_instance_type]['vcpus']
            remaining_memory = resources_required['memory'] - j * instances[current_instance_type]['memory']
            remaining_resources = {'vcpus': remaining_vcpus, 'memory': remaining_memory}
            
            # Calculate the cost of using the current instance count
            new_instance_count = current_instance_count + i
            new_cost = cost_so_far + i * instances[current_instance_type]['cost']
            
            # Recurse on the remaining instance types
            remaining_instance_types = instance_types[1:]
            cost = find_optimal_instance_combination(remaining_resources, remaining_instance_types, instance_counts, new_cost)
            if cost < min_cost:
                min_cost = cost
            
            # Update the count for the current instance type
            instance_counts[current_instance_type] = new_instance_count
    
    return min_cost

# Find the optimal combination of instances
instance_types = sorted(instances, key=lambda x: instances[x]['cost'])
instance_counts = {}
resources_required = {'vcpus': 4, 'memory': 6}
cost = find_optimal_instance_combination(resources_required, instance_types, instance_counts, 0)
print(f"Optimal cost: {cost}")
print(f"Instance counts: {instance_counts}")
