from costModel import helpers
# cost function

def fixedCost():
    data = helpers.readJson(".privateCost.json")
    server_cost = sum(data['fixedCost']['severCost'])
    network_cost = sum(data['fixedCost']['networkDeviceCost'])
    software_cost = sum(data['fixedCost']['softwareLicenseCost'])
    space_cost = data['fixedCost']['spaceCost']
    non_electric_cost = data['fixedCost']['nonElectricCost']
    Dit = data['fixedCost']['Dit']*30*24
    Df = data['fixedCost']['Df']*30*24
    Du = data['fixed']['Du']*30*24
    
    fixed_cost = (server_cost + network_cost + software_cost)/Dit + space_cost/Df + non_electric_cost/Du
    
    return fixed_cost

def variableCost():
    data = helpers.readJson(".privateCost.json")
    electricity_cost = data['electricityUnitCost'] * (data['Eidle'] + data['Erunning'])
    internet_cost = data['internetCost']
    labor_cost = data['laborCost']
    
    variable_cost = electricity_cost + internet_cost + labor_cost
    
    return variable_cost

def costPerNode(node_count):
    # considered all the nodes are homogeneous
    # calculate the both the fixed cost and the variable cost for all the servers per hour and devide it by the desired node count
    # node count need to be decided beforehand
    cost = fixedCost()/node_count + variableCost()/node_count
    return cost
    