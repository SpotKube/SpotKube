import os
import sys

dirs = ['optimizer', 'cost_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from optimization_engine.cost_model.publicModel import publicCost_v1
from optimization_engine.cost_model.privateModel import privateCost_v1, privateCost_v2
from optimization_engine.predictor import main
from utils import get_logger

from . import optimizerStrategy
from . import helper
from .bruteforce import bruteforce_v1, bruteforce_v2
from .greedy import greedy_v1, greedy_v2, greedy_v3
from .ga import pymoo_v2

current_dir = os.getcwd()
logger_dir = os.path.join(current_dir, "logs")

logger = get_logger(path=logger_dir, log_file="management_server.log")


dir_path = os.path.dirname(os.path.abspath(__file__))
spot_path = os.path.join(dir_path, '../.spotConfig.json')
private_path = os.path.join(dir_path, '../.privateConfig.json')
spot = helper.readJson(spot_path)
private = helper.readJson(private_path)

async def returnNodeConfiguration(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func):
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
        elif optimizer_strategy_name == "pymoo_v2":
            optimizer = optimizerStrategy.OptimizerStrategy(pymoo_v2.optimize)
        else:
            logger.error("Invalid optimizer strategy name")
            return {"message": "Invalid optimizer strategy name", "status": 500}

        # predict spot price and private node price if need
        main.predict()
        
        if optimizer is not None:
            spotNodes = optimizer.optimize(spot, False, publicCost_v1, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns)
            privateNodes = optimizer.optimize(private, True, private_cost_func, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns)
            helper.returnTf(spotNodes, False)
            helper.returnTf(privateNodes, True)
            logger.info("Optimization completed")
            return {"message": "Optimization completed", "status": 200, "spot": spotNodes, "private": privateNodes}
        else:
            logger.error("Failed to initialize optimizer")
            return {"message": "Failed to initialize optimizer", "status": 500}
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        print("Exception: ", e)
        logger.error("Error in optimization engine: {0}".format(e))
        return {"message": "Error in optimization engine", "status": 500}
    
    
   

     
    
