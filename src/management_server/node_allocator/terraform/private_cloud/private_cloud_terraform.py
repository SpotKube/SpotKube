import subprocess
import time
import json
import os

current_dir = os.getcwd()
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")
    
async def destroy_private_cloud():
    # Destroy resources
    # subprocess.run(["pwd"], cwd=terraform_dir)
    subprocess.run(["terraform", "destroy", "-auto-approve", "-var-file=private.tfvars"], cwd=terraform_dir)
    

async def destroy_and_provision_private_cloud():
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
    with open("private_instance_terraform_output.json", "w") as f:
        f.write(output)
    
    # Read the management node floating IP from the Terraform output
    with open("private_instance_terraform_output.json", "r") as f:
        data = json.load(f)
        management_node_floating_ip = data["private_management_floating_ip"]["value"]
        
    return {"management_node_floating_ip": management_node_floating_ip}

# Initialize Terraform and apply changes
async def provision_private_cloud():    
    # Initialize Terraform
    subprocess.run(["terraform", "init"], cwd=terraform_dir)
    
    return await apply_terraform()

# Apply changes
async def apply_private_cloud():
    return await apply_terraform()

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
    
    # Read the management node floating IP from the Terraform output
    with open("private_instance_terraform_output.json", "r") as f:
        data = json.load(f)
        management_node_floating_ip = data["private_management_floating_ip"]["value"]
        
    return {"management_node_floating_ip": management_node_floating_ip}