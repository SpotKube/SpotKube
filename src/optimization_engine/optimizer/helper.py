from collections import defaultdict

import json
import yaml
import os


dir_path = os.path.dirname(os.path.abspath(__file__))

def calculateResources(flag):
    pods = defaultdict(dict)
    file_path = os.path.join(dir_path, '../../../.config/config.yml')
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
        pods[service['name']]['pods'] = service['pods']
        pods[service['name']]['memory'] = round(int(service['pods']) * maxMemory, 2)
        pods[service['name']]['cpu'] = round(int(service['pods']) * maxCPU, 2)
        
    
    return pods, maxCPU, maxMemory


def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data

def returnTf(nodes, flag):
    tf = defaultdict(dict)
    if (nodes and len(nodes) > 0):
        if (flag):
            file_path = os.path.join(dir_path, '../.privateConfig.json')
            output_path = os.path.join(dir_path, '../output/private.tfvars')
            instances = readJson(file_path)
            for i in range(len(nodes)):
                tf['private_instances'][f'node-{i+1}'] = {
                    'region': 'us-east-1',
                    'instance_type': nodes[i],
                    'price': instances[nodes[i]]["cost"],
                }
        else:
            file_path = os.path.join(dir_path, '../.spotConfig.json')
            output_path = os.path.join(dir_path, '../output/spot.tfvars')
            instances = readJson(file_path)
            for i in range(len(nodes)):
                tf['spot_instances'][f'spot-{i+1}'] = {
                    'region': 'us-east-1',
                    'instance_type': nodes[i],
                    'spot_price': instances[nodes[i]]["cost"],
                }
        
        writeTf(output_path, tf)
    return tf

def writeTf(file, tf):
    with open(file, "w") as f:
        for key, value in tf.items():
            f.write(f"{key} = {{\n")
            for inner_key, inner_value in value.items():
                f.write(f"  \"{inner_key}\" = {{\n")
                for ik, iv in inner_value.items():
                    f.write(f"      {ik} = \"{iv}\"\n")
                f.write("},\n")
            f.write("}\n")

def readYml(file):
    with open(file, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data   
        except yaml.YAMLError as exc:
            print(exc)
            
def getPrivateNodeCount():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, '../../../.config/config.yml')
    data = readYml(file_path)
    node_count = data['resources']['privateResources']['nodeCount']
    return node_count