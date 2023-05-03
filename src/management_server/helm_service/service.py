import yaml
import os
import subprocess
from utils import run_subprocess_cmd, run_subprocess_popen_cmd, format_terraform_error_message, get_logger

current_dir = os.getcwd()
logger_dir = os.path.join(current_dir, "logs")

logger = get_logger(path=logger_dir, log_file="private_cloud_helm_service.log")

# configFilePath = os.path.join(os.path.dirname(__file__), 'config.yml')

async def deploy_helm_charts():
    try:
        # Load the config.yml file
        with open('~/.config/spotkube/config.yml') as f:
            config = yaml.safe_load(f)

        # Loop through each service and install the corresponding Helm chart
        for service in config['services']:
            helm_chart_path = service['helmChartPath']
            pod_count = service['minRPS']['pods']
            service_name = service['name']
            
            run_subprocess_popen_cmd(["helm", "upgrade", "--install", "--set", "replicaCount={pod_count}" "{helm_chart_path}"], cwd=current_dir)        
            # os.system(f"helm upgrade --install --set replicaCount={pod_count} {service_name} {helm_chart_path}")
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": "failed"}