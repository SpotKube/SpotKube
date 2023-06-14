from .optimizer.optimizerMain import returnNodeConfiguration

# Generate optimal node combination
def service_get_node_configuration(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func):
    return returnNodeConfiguration(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func)

