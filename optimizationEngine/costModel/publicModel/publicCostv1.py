from ..helpers import *

instances = readJson('../.spotConfig.json')
def cost(nodes):
    cost = sum(instances[node]['cost'] for node in nodes)
    return cost

    