import os
import time
import json
from python_terraform import *
import ansible.playbook
import ansible.constants

async def provision_private_cloud():
    terraform = Terraform()
    print("Hey Terraform")
    # Set the path to the Terraform configuration files
    terraform_dir = os.path.join(os.path.dirname(__file__), ".")

    # Load the Terraform variables from the configuration file
    tf_vars_file = os.path.join(terraform_dir, "private.tfvars")
    tf_vars = terraform.read_vars(tf_vars_file)

    # Initialize the Terraform configuration
    tf = terraform.Terraform(working_dir=terraform_dir)
    print("Initializing Terraform")
    # tf.init()

    # # Apply the Terraform configuration
    # tf.apply(
    #     skip_plan=True,
    #     var_file=tf_vars_file,
    #     auto_approve=True,
    # )

    # # Wait for 60 seconds to ensure the instances are fully provisioned
    #  # Wait for 60 seconds to ensure the instances are fully provisioned
    # await asyncio.sleep(60)

    # # Save the Terraform output to a JSON file
    # output = tf.output(json=True)
    # with open("private_instance_terraform_output.json", "w") as f:
    #     json.dump(output, f)