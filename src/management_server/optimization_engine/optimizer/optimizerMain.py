import os
import sys

dirs = ['optimizer', 'cost_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from optimization_engine.cost_model.publicModel import publicCost_v1
from optimization_engine.cost_model.privateModel import privateCost_v1

from . import optimizerStrategy
from . import helper
from .bruteforce import bruteforce_v1, bruteforce_v2
from .greedy import greedy_v1, greedy_v2, greedy_v3

dir_path = os.path.dirname(os.path.abspath(__file__))
spot_path = os.path.join(dir_path, '../.spotConfig.json')
private_path = os.path.join(dir_path, '../.privateConfig.json')
spot = helper.readJson(spot_path)
private = helper.readJson(private_path)

async def returnNodeConfiguration(optimizer_strategy_name):
    try :
        optimizer = None
        if optimizer_strategy_name == "bruteforce_v1":
            optimizer = optimizerStrategy.OptimizerStrategy(bruteforce_v1.optimize)
        elif optimizer_strategy_name == "bruteforce_v2":
            optimizer = optimizerStrategy.OptimizerStrategy(bruteforce_v2.optimize)
        elif optimizer_strategy_name == "greedy_v1":
            optimizer = optimizerStrategy.OptimizerStrategy(greedy_v1.optimize)
        elif optimizer_strategy_name == "greedy_v2":
            optimizer = optimizerStrategy.OptimizerStrategy(greedy_v2.optimize)
        elif optimizer_strategy_name == "greedy_v3":
            optimizer = optimizerStrategy.OptimizerStrategy(greedy_v3.optimize)
        else:
            return {"message": "Invalid optimizer strategy name", "status": 500}

        if optimizer is not None:
            spotNodes = optimizer.optimize(spot, False, publicCost_v1, [])
            privateNodes = optimizer.optimize(private, True, privateCost_v1, [])
            helper.returnTf(spotNodes, False)
            helper.returnTf(privateNodes, True)
            return {"message": "Optimization completed", "status": 200, "spot": spotNodes, "private": privateNodes}
        else:
            return {"message": "Failed to initialize optimizer", "status": 500}
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {"message": "Error in optimization engine", "status": 500}
    
    
   

     
    
