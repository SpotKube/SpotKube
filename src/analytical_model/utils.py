from collections import defaultdict

import json
import yaml
import os
from ruamel.yaml import YAML

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, '../../.config/config.yml')

def getMinRps():
    services = []
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for service in data['services']:
                services.append({'name':service['name'], 'minRps': service['minRPS']['rps']})
        except yaml.YAMLError as exc:
            print(exc)    
    
    return services


def updatePodCount(service, count):
    yaml_ruamel=YAML(typ='safe')
    yaml_ruamel.default_flow_style = False
    yaml_ruamel.preserve_quotes = True
    yaml_ruamel.sort_keys = False
    try:
        with open(file_path, 'r') as f:
            data = yaml_ruamel.load(f)
        
        for serviceDic in data['services']:
            if(service == serviceDic['name']):
                serviceDic['minRPS']['pods'] = count
                break
        with open(file_path, 'w') as f:
            yaml_ruamel.dump(data,f)
    except yaml_ruamel.YAMLError as exc:
        print(exc)