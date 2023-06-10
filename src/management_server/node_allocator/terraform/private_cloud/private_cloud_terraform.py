import subprocess
import time
import os
from utils import get_logger, format_terraform_error_message, run_subprocess_cmd

current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")
logger_dir = os.path.join(current_dir, "logs")

private_provisioning_logger = get_logger(path=logger_dir, log_file="private_cloud_terraform.log")
    
# Destroy private cloud
async def destroy_private_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        private_provisioning_logger.info("Private cloud destroyed")
        return {"message": "Private cloud destroyed", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    

# Destroy and provision private cloud
async def destroy_and_provision_private_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
        # Initialize Terraform
        run_subprocess_cmd(["terraform", "init"], cwd=terraform_dir)
        
        # Apply terraform
        await apply_terraform()
        
        private_provisioning_logger.info("Destroy and provisioning completed")
        return {"message": "Destroy and provisioning completed", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    
# Initialize Terraform and apply changes
async def provision_private_cloud():  
    try:  
        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd=terraform_dir)
        await apply_terraform()
        
        private_provisioning_logger.info("Private cloud provisioned")
        return {"message": "Private cloud provisioned", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}

# Apply changes
async def apply_private_cloud():
    try:
        await apply_terraform()
        private_provisioning_logger.info("Private cloud changes applied")
        return {"message": "Private cloud changes applied", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        error_message = format_terraform_error_message(str(error_message))
        print("Hey this is error",error_message)
        private_provisioning_logger.error(error_message)
        return {"error_message": "error_message", "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}

# Private function to apply changes
async def apply_terraform():
    try:
        # Apply changes
        run_subprocess_cmd(["terraform", "apply", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
        # Wait for instances to be provisioned
        time.sleep(60)
        
        # Save Terraform output to a JSON file
        output = run_subprocess_cmd(["terraform", "output", "-json"], cwd=terraform_dir)
        
        with open(f"{terraform_dir}/private_instance_terraform_output.json", "w") as f:
            f.write(output)
            
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
# Private function to apply changes
async def write_terraform_output():
    try:
        output = run_subprocess_cmd(["terraform", "output", "-json"], cwd=terraform_dir)
        
        with open(f"{terraform_dir}/private_instance_terraform_output.json", "w") as f:
            f.write(output)
        return {"message": "Terraform output written to file", "status": 200}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_provisioning_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    