import helpers
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, '../../../.config/privateCost.json')
data = helpers.readJson(file_path)

def fixedCost():
    server_cost = sum(data['fixedCost']['serverCost'])
    network_cost = sum(data['fixedCost']['networkDeviceCost'])
    software_cost = sum(data['fixedCost']['softwareLicenseCost'])
    space_cost = data['fixedCost']['spaceCost']
    non_electric_cost = data['fixedCost']['nonElectricCost']
    Dit = data['fixedCost']['Dit']*30*24
    Df = data['fixedCost']['Df']*30*24
    Du = data['fixedCost']['Du']*30*24
    
    fixed_cost = (server_cost + network_cost + software_cost)/Dit + space_cost/Df + non_electric_cost/Du
    
    return fixed_cost

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
    node_count = helpers.getPrivateNodeCount()
    cost = fixedCost()/node_count + variableCost()/node_count
    return cost

def cost(nodes):
    total_cost = len(nodes) * costPerNode()
    return total_cost