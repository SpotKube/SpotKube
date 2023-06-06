from .optimizer.optimizerMain import returnNodeConfiguration

# Generate optimal node combination
def service_get_node_configuration(optimizer_strategy_name):
    return returnNodeConfiguration(optimizer_strategy_name)

