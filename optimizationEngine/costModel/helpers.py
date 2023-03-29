import json

def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data