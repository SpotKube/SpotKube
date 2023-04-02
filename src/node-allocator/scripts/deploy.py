import yaml
import os

# configFilePath = os.path.join(os.path.dirname(__file__), 'config.yml')

# Load the config.yml file
with open('../../../.config/config.yml') as f:
    config = yaml.safe_load(f)

# Loop through each service and install the corresponding Helm chart
for service in config['services']:
    helm_chart_path = service['helmChartPath']
    pod_count = service['minRPS']['pods']
    service_name = service['name']
    
    os.system(f"helm upgrade --install --set replicaCount={pod_count} {service_name} {helm_chart_path}")