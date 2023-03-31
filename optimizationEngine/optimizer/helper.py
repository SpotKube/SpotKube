from collections import defaultdict

import json
import yaml

def calculateResources():
    pods = defaultdict(dict)
    with open("/home/due/Documents/ACA/Sem 7/Research/SpotKube/.config/config.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            maxCPU = data['resources']['pods']['maxCPU']
            maxMemory = data['resources']['pods']['maxMemory']
            services = [{'name':service['name'], 'pods': service['minRPS']['pods']} for service in data['services']]
        except yaml.YAMLError as exc:
            print(exc)
    
    for service in services:
        pods[service['name']]['memory'] = round(int(service['pods']) * maxMemory, 2)
        pods[service['name']]['cpu'] = round(int(service['pods']) * maxCPU, 2)
    
    return pods


def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data

calculateResources()