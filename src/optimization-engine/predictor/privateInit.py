import helpers as predictorutils
import os
import sys

dirs = ['costModel']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from privateModel import privateCost_v1
  
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, '../../.config/user_config.yml')
data = predictorutils.readYml(file_path)

private_config = os.path.join(dir_path, '../.privateConfig.json')
config = predictorutils.readJson(private_config)

def updatePrivateConfig():
    nodeCPU = data['privateResources']['nodeCPU']
    nodeMemory = data['privateResources']['nodeMemory']
    print(nodeCPU, nodeMemory)
    predictorutils.updateJson(private_config, list(config)[0], nodeCPU, nodeMemory)
    # privateCost_v1.costPerNode() // There is an import error when calculating cost of private node.

updatePrivateConfig()