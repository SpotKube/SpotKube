import os
from optimization_engine.cost_model.helpers import *

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, '../../.spotConfig.json')
instances = readJson(file_path)

def cost(nodes):
    cost = 0
    if (nodes):
        cost = sum(instances[node]['cost'] for node in nodes)
    return cost

    