import yaml
import os
import subprocess
import time
from utils import run_subprocess_cmd, run_subprocess_popen_cmd, format_terraform_error_message, get_logger

current_dir = os.getcwd()
logger_dir = os.path.join(current_dir, "logs")

helm_service_logger = get_logger(path=logger_dir, log_file="helm_service.log")

# configFilePath = os.path.join(os.path.dirname(__file__), 'config.yml')

async def deploy_helm_charts(privateCloud=False):
    try:
        # Load the config.yml file
        CONFIG_PATH = "~/.config/spotkube/config.yml"
        file_path = os.path.expanduser(CONFIG_PATH)
        with open(file_path) as f:
            config = yaml.safe_load(f)
            
        if privateCloud:
            helm_service_logger = get_logger(path=logger_dir, log_file="private_cloud_helm_service.log")
        else:
            helm_service_logger = get_logger(path=logger_dir, log_file="aws_cloud_helm_service.log")

        # Loop through each service and install the corresponding Helm chart
        for service in config['services']:
            cloud = service['private']
            if privateCloud != cloud:
                continue
            
            helm_chart_path = service['helmChartPath']
            pod_count = service['minRPS']['pods']
            service_name = service['name']
            
            helm_chart_path = os.path.expanduser(helm_chart_path)
            run_subprocess_popen_cmd(["helm", "install", "--namespace" ,"default", "--set", f"replicaCount={pod_count}", helm_chart_path, "--generate-name"], cwd=current_dir)        
            # os.system(f"helm upgrade --install --set replicaCount={pod_count} {service_name} {helm_chart_path}")
        
        helm_service_logger.info("Deployed successfully")
        return {"status": 200, "message": "Deployed successfully"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        helm_service_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        helm_service_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
