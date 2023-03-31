from collections import defaultdict

import json
import yaml
import os

def calculateResources(flag):
    pods = defaultdict(dict)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, '../../.config/config.yml')
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            maxCPU = data['resources']['pods']['maxCPU']
            maxMemory = data['resources']['pods']['maxMemory']
            # services = [{'name':service['name'], 'pods': service['minRPS']['pods']} for service in data['services'] and service['private'] == private]
            services = []
            for service in data['services']:
                if service['private'] == flag:
                    services.append({'name':service['name'], 'pods': service['minRPS']['pods']})
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