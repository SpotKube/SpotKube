import json
import yaml

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
    data = readYml("/home/due/Documents/ACA/Sem 7/Research/SpotKube/.config/user_config.yml")
    nodeCount = data['privateResources']['nodeCount']
    return nodeCount