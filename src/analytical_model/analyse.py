import os
import sys
dirs = ['analytical_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)
from pod_calculator import calculator
import utils

from metric_analyser import cpuAnalyser, memoryAnalyser, preprocess
# Iterate thorugh directories in outputs directory
for service in os.listdir('../load_testing/outputs'):
    serviceTuple = calculator.calculate(service)
    print(serviceTuple)
    utils.updatePodCount(serviceTuple[0], serviceTuple[1])
