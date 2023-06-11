import os
import json
import subprocess

from utils import get_logger, format_terraform_error_message, run_subprocess_popen_cmd, run_subprocess_cmd

current_dir = os.getcwd()
ansible_dir = os.path.join(current_dir, "node_allocator", "ansible", "public_cloud")
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "aws")
logger_dir = os.path.join(current_dir, "logs")

public_configure_logger = get_logger(path=logger_dir, log_file="aws_cloud_ansible.log")

async def generate_aws_cloud_hosts_file():
    try:
        # Read control_plane_ip and worker_ips from input.json using jq
        with open(f"{terraform_dir}/aws_instance_terraform_output.json") as f:
            output = json.load(f)
            control_plane_ip = output['master_node_ip']['value']
            worker_ips = [worker['private_ip'] for worker in output['spot_instances']['value']]
            
        key_name = "id_rsa"

        # Write the Ansible hosts file
        with open(f'{ansible_dir}/hosts', 'w') as f:
            f.write('[control_plane]\n')
            f.write(f'{control_plane_ip}\n\n')
            f.write('[workers]\n')
            for worker_ip in worker_ips:
                f.write(f'{worker_ip}\n')
            f.write('\n')
            f.write('[control_plane:vars]\n')
            f.write('ansible_connection=ssh\n')
            f.write('ansible_user=ubuntu\n')
            f.write(f'ansible_ssh_aws_key_file=~/.ssh/{key_name}\n\n')
            f.write('[workers:vars]\n')
            f.write('ansible_connection=ssh\n')
            f.write('ansible_user=ubuntu\n')
            f.write(f'ansible_ssh_aws_key_file=~/.ssh/{key_name}\n')
        
        public_configure_logger.info("Host file generated") 
        return {"message": "Ansible hosts file generated", "status": 200}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        public_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
        
async def configure_aws_nodes():
    try:
        # Generate the Ansible hosts file
        res = await generate_aws_cloud_hosts_file()
        if (res["status"] != 200):
            return res
        
        run_subprocess_popen_cmd(["bash", "ansible_run.sh"], cwd=ansible_dir)
        
        # # Run the initial playbook
        # run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "initial.yml"], cwd=ansible_dir)
        
        # # Run the kube-dependencies playbook
        # run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "kube_dependencies.yml"], cwd=ansible_dir)
        
        # # Run the control-plane playbook
        # run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "control_plane.yml"], cwd=ansible_dir)

        # # Run the worker playbook
        # run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "workers.yml"], cwd=ansible_dir)

        # # Run the setup_kubectl playbook
        # run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "setup_kubectl.yml"], cwd=ansible_dir)
        
        public_configure_logger.info("Aws cloud nodes configured")
        
        return {"message": "Nodes configured", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        public_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        public_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}

