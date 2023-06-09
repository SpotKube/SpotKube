from .optimizer.optimizerMain import returnNodeConfiguration

# Generate optimal node combination
def service_get_node_configuration(optimizer_strategy_name, services_list, allocated_nodes, private_cost_func):
    return returnNodeConfiguration(optimizer_strategy_name, services_list, allocated_nodes, private_cost_func)

