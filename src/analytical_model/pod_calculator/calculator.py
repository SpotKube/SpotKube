import os
import sys
import math

dirs = ['analytical_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from metric_analyser import cpuAnalyser, memoryAnalyser, preprocess
import utils

def calculate(service):
    serviceConfig = {}
    services = utils.getMinRps()
    df_cpu = preprocess.preprocess(service)

    cpu_throttle_rps = cpuAnalyser.analyse(df_cpu) # assuming cpu throttling rps for each service
    # mem_throttle_rps = memoryAnalyser.analyse(df_mem) # assuming memory throttling rps for each service
    
    for serviceDic in services:
        if(service == serviceDic['name']):
            serviceConfig = serviceDic
            break
    cpu_count = math.ceil(serviceConfig['minRps']/ cpu_throttle_rps)
    mem_count = 0 # math.ceil(service['minRps']/ mem_throttle_rps[service['name']]['rps'])
    count = max(cpu_count, mem_count)
    # pod_count.append({'name': service['name'], 'podCount': count}) # assuming the resource limitaion for  load testing pod and actual deploying pod are equal

    return (service, count)



