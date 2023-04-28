import subprocess
import time
import json
import os

current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")
    
async def destroy_private_cloud():
    try:
        # Destroy resources
        subprocess.run(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        return {"message": "Private cloud destroyed"}
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        with open(f"{terraform_dir}/terraform_error_output.txt", "w") as f:
            f.write(error_message)
        return {"error_message": error_message}
    

async def destroy_and_provision_private_cloud():
    try:
        # Destroy resources
        subprocess.run(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
        # Initialize Terraform
        subprocess.run(["terraform", "init"])
        
        # Apply changes
        subprocess.run(["terraform", "apply", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
        
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