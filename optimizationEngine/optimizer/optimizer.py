import optimizerStrategy
from bruteforce import bruteforce1
from . import helper
from ..costModel.publicModel import publicCostv1

# Define the available node types and their prices
instances = helper.readJson('../.spotConfig.json')

def main():
    optimizer = optimizerStrategy.OptimizerStrategy(bruteforce1.optimize)
    optimizer.optimize(instances, publicCostv1)
    
if __name__ == "__main__":
    main()
    

