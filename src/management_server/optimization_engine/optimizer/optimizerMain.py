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

async def returnNodeConfiguration():
    try :
        optimizer = optimizerStrategy.OptimizerStrategy(greedy_v2.optimize)
        spotNodes = optimizer.optimize(spot, False, publicCost_v1, [])
        privateNodes = optimizer.optimize(private, True, privateCost_v1, [])
        
        helper.returnTf(spotNodes, False)
        helper.returnTf(privateNodes, True)
        return {"message": "Optimization completed", "status": "success"}
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {"message": "Error in optimization engine", "status": "failed"}
    finally:
        return {"message": "Error in optimization engine", "status": "failed"}
    
   

     
    
