from collections import defaultdict

import json
import yaml
import os
from ruamel.yaml import YAML

dir_path = os.path.dirname(os.path.abspath(__file__))


def getMinRps():
    file_path = os.path.join(dir_path, '../../.config/user_config.yml')
    services = []
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for service in data['services']:
                services.append({'name':service['name'], 'minRPS': service['minRPS'], 'private': service['private'], 'helmChartPath': service['helmChartPath']})
        except yaml.YAMLError as exc:
            print(exc)    
    
    return services


def updatePodCount(service, count, rps, private, helmChartPath):
    file_path = os.path.join(dir_path, '../../.config/config.yml')
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
                serviceDic['minRPS']['rps'] = rps
                serviceDic['private'] = private
                serviceDic['helmChartPath'] = helmChartPath
                break
        else:
            data['services'].append({'name': service, 'minRPS': {'pods': count, 'rps': rps}, 'private': private})
        with open(file_path, 'w') as f:
            yaml_ruamel.dump(data,f)
    except yaml_ruamel.YAMLError as exc:
        print(exc)
