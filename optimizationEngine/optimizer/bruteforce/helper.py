import yaml
from collections import defaultdict

def calculateResources(services):
    pods = defaultdict(dict)
    with open("../../../config.yml", "r") as stream:
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

# def main():
#     service_requirements = {
#     'Service 1': {'pods': 3,},
#     'Service 2': {'pods': 5}
#     }
#     print(calculateResources(service_requirements))
    