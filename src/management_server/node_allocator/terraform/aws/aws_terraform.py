import subprocess
import time
import os
from utils import get_logger, format_terraform_error_message, run_subprocess_cmd

current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "aws")
logger_dir = os.path.join(current_dir, "logs")

logger = get_logger(path=logger_dir, log_file="aws_terraform.log")
    
# Destroy aws cloud
async def destroy_aws_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=spot.tfvars"], cwd=terraform_dir)
        logger.info("Aws cloud destroyed")
        return {"message": "Aws cloud destroyed", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    

# Destroy and provision aws cloud
async def destroy_and_provision_aws_cloud():
    try:
        # Destroy resources
        run_subprocess_cmd(["terraform", "destroy", "-auto-approve", "-var-file=spot.tfvars"], cwd=terraform_dir)
        
        # Initialize Terraform
        run_subprocess_cmd(["terraform", "init"], cwd=terraform_dir)
        
        # Apply terraform
        result = await apply_terraform()
        if(result["status"] != 200):
            return result
        
        logger.info("Destroy and provisioning completed")
        return {"message": "Destroy and provisioning completed", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    
# Initialize Terraform and apply changes
async def provision_aws_cloud():  
    try:  
        # Initialize Terraform
        run_subprocess_cmd(["terraform", "init"], cwd=terraform_dir)
        result = await apply_terraform()
        if(result["status"] != 200):
            return result
        
        logger.info("Aws cloud provisioned")
        return {"message": "Aws cloud provisioned", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}

# Apply changes
async def apply_aws_cloud():
    try:
        result = await apply_terraform()
        if(result["status"] != 200):
            logger.error(result["error_message"])
            return {"error_message": result["error_message"], "status": 500}
            
        logger.info("Aws cloud changes applied")
        return {"message": "Aws cloud changes applied", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        error_message = format_terraform_error_message(str(error_message))
        print("Hey this is error",error_message)
        logger.error(error_message)
        return {"error_message": "error_message", "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}

# Aws function to apply changes
async def apply_terraform():
    try:
        # Apply changes
        run_subprocess_cmd(["terraform", "apply", "-auto-approve", "-var-file=spot.tfvars"], cwd=terraform_dir)
        
        # Wait for instances to be provisioned
        time.sleep(60)
        
        # Save Terraform output to a JSON file
        output = run_subprocess_cmd(["terraform", "output", "-json"], cwd=terraform_dir)
        
        with open(f"{terraform_dir}/aws_instance_terraform_output.json", "w") as f:
            f.write(output)
        return {"message": "Aws cloud changes applied", "status": 200}
        
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
# Aws function to apply changes
async def write_terraform_output():
    try:
        output = run_subprocess_cmd(["terraform", "output", "-json"], cwd=terraform_dir)
        
        with open(f"{terraform_dir}/aws_instance_terraform_output.json", "w") as f:
            f.write(output)
        return {"message": "Terraform output written to file", "status": 200}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    