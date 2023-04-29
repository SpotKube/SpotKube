import subprocess
import os
import json
from utils import get_logger, format_terraform_error_message, run_subprocess_cmd

current_dir = os.getcwd()
ansible_dir = os.path.join(current_dir, "node_allocator", "ansible")
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")

async def generate_private_cloud_hosts_file():
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

    print(key_name)

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
        
def configure_private_nodes():
    # Generate the Ansible hosts file
    generate_private_cloud_hosts_file()
    
    # Run the initial playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "initial.yml"], cwd=ansible_dir)
    print(output)
    
    # Run the kube-dependencies playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "kube_dependencies.yml"], cwd=ansible_dir)
    print(output)
    
    # Run the control-plane playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "control_plane.yml"], cwd=ansible_dir)
    print(output)
    
    return {"message": "Nodes configured", "status": "success"}

        
