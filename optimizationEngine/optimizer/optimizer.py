import os
import sys

dirs = ['optimizer', 'costModel']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

import optimizerStrategy
from bruteforce import bruteforce_v1
import helper
from publicModel import publicCost_v1
from privateModel import privateCost_v1

# Define the available node types and their prices
dir_path = os.path.dirname(os.path.abspath(__file__))
spot_path = os.path.join(dir_path, '../.spotConfig.json')
private_path = os.path.join(dir_path, '../.privateConfig.json')
spot = helper.readJson(spot_path)
private = helper.readJson(private_path)

def main():
    optimizer = optimizerStrategy.OptimizerStrategy(bruteforce_v1.optimize)
    optimizer.optimize(spot, publicCost_v1, False)
    optimizer.optimize(private, privateCost_v1, True)
    
if __name__ == "__main__":
    main()
    
    

