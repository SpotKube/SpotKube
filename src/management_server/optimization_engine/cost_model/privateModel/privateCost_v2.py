import optimization_engine.cost_model.helpers as costutils
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = '~/.config/spotkube/privateCost.json'
file_path = os.path.expanduser(CONFIG_PATH)

# file_path = os.path.join(dir_path, '../../../../.config/privateCost.json')
data = costutils.readJson(file_path)

config_path = os.path.join(dir_path, '../../.privateConfig.json')
config = costutils.readJson(config_path)


def variableCost():
    electricity_cost = data['variableCost']['electricityUnitCost'] * (data['variableCost']['Eidle'] + data['variableCost']['Erunning'])
    internet_cost = data['variableCost']['internetCost']
    labor_cost = data['variableCost']['laborCost']
    
    variable_cost = electricity_cost + internet_cost + labor_cost
    
    return variable_cost

def costPerNode():
    # considered all the nodes are homogeneous
    # calculated both the fixed cost and the variable cost for all the servers per hour and devide it by the desired node count
    # node count need to be decided beforehand
    node_count = costutils.getPrivateNodeCount()
    cost = variableCost()/node_count
    costutils.updateJson(config_path, list(config)[0], round(cost, 3))
    return round(cost, 3)

def cost(nodes):
    total_cost = 0
    if (nodes):
        current_cost = config[list(config)[0]]['cost']
        if (current_cost == 0 or current_cost == None):
            total_cost = costPerNode() * len(nodes)
        else:
            total_cost = current_cost * len(nodes)
    return total_cost
