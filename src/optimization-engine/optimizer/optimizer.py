import os
import sys

dirs = ['optimizer', 'cost-model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from publicModel import publicCost_v1
from privateModel import privateCost_v1
import optimizerStrategy
import helper
from bruteforce import bruteforce_v1, bruteforce_v2
from greedy import greedy_v1

dir_path = os.path.dirname(os.path.abspath(__file__))
spot_path = os.path.join(dir_path, '../.spotConfig.json')
private_path = os.path.join(dir_path, '../.privateConfig.json')
spot = helper.readJson(spot_path)
private = helper.readJson(private_path)

def main():
    optimizer = optimizerStrategy.OptimizerStrategy(greedy_v1.optimize)
    spotNodes = optimizer.optimize(spot, False, publicCost_v1)
    privateNodes = optimizer.optimize(private, True, privateCost_v1)
    
    helper.returnTf(spotNodes, False)
    helper.returnTf(privateNodes, True)
    
if __name__ == "__main__":
    main()
    
    
