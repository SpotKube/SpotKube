import subprocess
import time
import json
import os
import re

import logging


current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(f"{terraform_dir}/terraform.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def format_terraform_error_message(error_message):
    # Replace escape characters with their printable equivalents
    error_message = error_message.replace('\n\n\n', '\n')
    error_message = error_message.replace('\n\n', '\n')
    error_message = error_message.replace('\u001b[1m', '')
    error_message = error_message.replace('\u001b[0m', '')
    error_message = error_message.replace('│\n \n', '')
    error_message = error_message.replace('╷\n\n', '')
    formatted_message = re.sub(r'\x1b\[\d+m', '', error_message)
    return str(formatted_message)

def run_command(command, cwd):
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error = result.stderr.decode('utf-8')
        raise Exception(error if error  else "Internal Server Error")
    return result.stdout.decode('utf-8')
    
async def destroy_private_cloud():
    try:
        # Destroy resources
        output = run_command(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        print(output)
        logger.info("Private cloud destroyed")
        return {"message": "Private cloud destroyed"}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        error_message = format_terraform_error_message(str(e))
        logger.exception(error_message)
        with open(f"{terraform_dir}/terraform_error_output.txt", "w") as f:
            f.write(error_message)
        return {"error_message": error_message}
    
    except  Exception as e:
        # Print and Log the error message and return it
        print(e)
        error_message = format_terraform_error_message(str(e))
        logger.error(error_message)
        return {"error_message": str(e)}
    

async def destroy_and_provision_private_cloud():
    try:
        # Destroy resources
        run_command(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
        # Initialize Terraform
        run_command(["terraform", "init"])
        
        # Apply changes
        run_command(["terraform", "apply", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
        # Wait for instances to be provisioned
        time.sleep(60)
        
        # Save Terraform output to a JSON file
        output = subprocess.check_output(["terraform", "output", "-json"]).decode("utf-8")
        with open(f"{terraform_dir}/private_instance_terraform_output.json", "w") as f:
            f.write(output)
        
        # Read the management node floating IP from the Terraform output
        with open(f"{terraform_dir}/private_instance_terraform_output.json", "r") as f:
            data = json.load(f)
            management_node_floating_ip = data["private_management_floating_ip"]["value"]
            
        return {"management_node_floating_ip": management_node_floating_ip}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        with open(f"{terraform_dir}/terraform_error_output.txt", "w") as f:
            f.write(error_message)
        return {"error_message": error_message}
    
    
# Initialize Terraform and apply changes
async def provision_private_cloud():  
    try:  
        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd=terraform_dir)
        await apply_terraform()
        return {"message": "Private cloud provisioned"}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        with open(f"{terraform_dir}/terraform_error_output.txt", "w") as f:
            f.write(error_message)
        return {"error_message": error_message}

# Apply changes
async def apply_private_cloud():
    try:
        await apply_terraform()
        return {"message": "Private cloud changes applied"}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        with open(f"{terraform_dir}/terraform_error_output.txt", "w") as f:
            f.write(error_message)
        return {"error_message": error_message}

# Private function to apply changes
async def apply_terraform():
    # Apply changes
    subprocess.run(["terraform", "apply", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
    
    # Wait for instances to be provisioned
    time.sleep(60)
    
    # Save Terraform output to a JSON file
    output = subprocess.check_output(["terraform", "output", "-json"]).decode("utf-8")
    with open("private_instance_terraform_output.json", "w") as f:
        f.write(output)