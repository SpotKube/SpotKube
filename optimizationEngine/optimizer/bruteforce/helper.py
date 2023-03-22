from collections import defaultdict

import json
import yaml

def calculateResources(services):
    pods = defaultdict(dict)
    with open("../../config.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            maxCPU = data['resources']['pods']['maxCPU']
            maxMemory = data['resources']['pods']['maxMemory']
        except yaml.YAMLError as exc:
            print(exc)
    for service in services.keys():
        pods[service]['memory'] = round(services[service]['pods'] * maxMemory, 2)
        pods[service]['cpu'] = round(services[service]['pods'] * maxCPU, 2)
    
    print(pods)
    return pods


def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data
    