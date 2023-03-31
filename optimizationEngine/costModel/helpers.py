import json
import yaml
import os

def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data

def readYml(file):
    with open(file, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data   
        except yaml.YAMLError as exc:
            print(exc)
            
def getPrivateNodeCount():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, '../../.config/user_config.yml')
    data = readYml(file_path)
    nodeCount = data['privateResources']['nodeCount']
    return nodeCount