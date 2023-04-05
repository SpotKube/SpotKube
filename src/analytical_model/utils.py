from collections import defaultdict

import json
import yaml
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

def getMinRps():
    file_path = os.path.join(dir_path, '../../../.config/config.yml')
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            services = []
            for service in data['services']:
                services.append({'name':service['name'], 'minRps': service['minRPS']['rps']})
        except yaml.YAMLError as exc:
            print(exc)    
    
    return services



