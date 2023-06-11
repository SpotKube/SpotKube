import os
import json
import subprocess

from utils import get_logger, format_terraform_error_message, run_subprocess_popen_cmd

current_dir = os.getcwd()
ansible_dir = os.path.join(current_dir, "node_allocator", "ansible", "private_cloud")
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")
logger_dir = os.path.join(current_dir, "logs")

private_configure_logger = get_logger(path=logger_dir, log_file="private_cloud_ansible.log")

async def generate_private_cloud_hosts_file():
    try:
        # Read control_plane_ip and worker_ips from input.json using jq
        with open(f"{terraform_dir}/private_instance_terraform_output.json") as f:
            output = json.load(f)
            control_plane_ip = output['private_master_ip']['value']
            worker_ips = [worker['private_ip'] for worker in output['private_workers']['value']]
            
        CONFIG_PATH = '~/.config/spotkube/provisioner.conf'
        config_path_expanded = os.path.expanduser(CONFIG_PATH)
        key_name = None

        with open(config_path_expanded, "r") as f:
            for line in f:
                if line.startswith("PRIVATE_INSTANCE_SSH_KEY_PATH="):
                    key_path = line.strip().split("=")[1]
                    key_name = key_path.split("/")[-1].replace("'", "")

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
            f.write(f'ansible_ssh_private_key_file=~/.ssh/{key_name}\n\n')
            f.write('[workers:vars]\n')
            f.write('ansible_connection=ssh\n')
            f.write('ansible_user=ubuntu\n')
            f.write(f'ansible_ssh_private_key_file=~/.ssh/{key_name}\n')
            
        return {"message": "Ansible hosts file generated", "status": 200}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
        
async def configure_private_nodes():
    try:
        # Generate the Ansible hosts file
        await generate_private_cloud_hosts_file()
        
        # Run the initial playbook
        run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "initial.yml"], cwd=ansible_dir)
        
        # Run the kube-dependencies playbook
        run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "kube_dependencies.yml"], cwd=ansible_dir)
        
        # Run the control-plane playbook
        run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "control_plane.yml"], cwd=ansible_dir)

        # Run the worker playbook
        run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "workers.yml"], cwd=ansible_dir)

        # Run the setup_kubectl playbook
        run_subprocess_popen_cmd(["ansible-playbook", "-i", "hosts", "setup_kubectl.yml"], cwd=ansible_dir)
        
        private_configure_logger.info("Private cloud nodes configured")
        
        return {"message": "Nodes configured", "status": 200}
    
    except subprocess.CalledProcessError as e:
        # Log the error message and return it
        error_message = e.output.decode("utf-8")
        print(error_message)
        error_message = format_terraform_error_message(str(error_message))
        private_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}
    
    except  Exception as error:
        print(error)
        error_message = format_terraform_error_message(str(error))
        private_configure_logger.error(error_message)
        return {"error_message": error_message, "status": 500}

