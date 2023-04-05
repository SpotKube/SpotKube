import os
import sys
import math

dirs = ['analytical_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

from metric_analyser import cpuAnalyser, memoryAnalyser, preprocess
import utils

def calculate():
    pod_count = []
    services = utils.getMinRps()
    df_cpu, df_mem = preprocess.preprocess()
    cpu_throttle_rps = cpuAnalyser.analyze(df_cpu) # assuming cpu throttling rps for each service
    mem_throttle_rps = memoryAnalyser.analyze(df_mem) # assuming memory throttling rps for each service
    
    for service in services:
        cpu_count = math.ceil(service['minRps']/ cpu_throttle_rps[service['name']]['rps'])
        mem_count = math.ceil(service['minRps']/ mem_throttle_rps[service['name']]['rps'])
        count = max(cpu_count, mem_count)
        pod_count.append({'name': service['name'], 'podCount': count}) # assuming the resource limitaion for  load testing pod and actual deploying pod are equal
    
    return pod_count



