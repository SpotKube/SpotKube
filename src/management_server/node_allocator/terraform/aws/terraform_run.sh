#! /bin/bash

# Import common functions
source ../../../scripts/common.sh

# Help function
function help() {
    print_info "Usage:"
    echo "  -d, --destroy                       Destroy the aws cloud environment"
    echo "  -db, --destroy_build                Destroy and build the aws cloud environment"
    echo "  -r, --reconfigure                   Reconfigure the aws cloud environment"
    echo "  -c, --configure                     Configure the aws cloud environment"
}

print_title "Provisioning public cloud environment"

# ------------------------------------- Check if required files exists ---------------------------------------------- #
CONF_FILE_ERROR=false

# Check if provisioner.conf exists
if [[ ! -f "../../../../.config/provisioner.conf" ]]; then
    print_error "provisioner.conf does not exist"
    CONF_FILE_ERROR=true
    exit 1
else
    source "../../../../.config/provisioner.conf"
fi

# Check if AWS_SHARED_CONFIG_FILE_PATH is set and exists
if [[ -z "$AWS_SHARED_CONFIG_FILE_PATH" ]]; then
    print_error "AWS_SHARED_CONFIG_FILE_PATH is not set in provisioner.conf"
    CONF_FILE_ERROR=true
elif [[ ! -f "$AWS_SHARED_CONFIG_FILE_PATH" ]]; then
    print_error "AWS_SHARED_CONFIG_FILE_PATH ($AWS_SHARED_CONFIG_FILE_PATH) does not exist"
    CONF_FILE_ERROR=true
fi

# Check if AWS_SHARED_CREDENTIALS_FILE_PATH is set and exists
if [[ -z "$AWS_SHARED_CREDENTIALS_FILE_PATH" ]]; then
    print_error "AWS_SHARED_CREDENTIALS_FILE_PATH is not set in provisioner.conf"
    CONF_FILE_ERROR=true
elif [[ ! -f "$AWS_SHARED_CREDENTIALS_FILE_PATH" ]]; then
    print_error "AWS_SHARED_CREDENTIALS_FILE_PATH ($AWS_SHARED_CREDENTIALS_FILE_PATH) does not exist"
    CONF_FILE_ERROR=true
fi

if $CONF_FILE_ERROR 
then
    exit 1
fi

# ---------------------------------- Check if required software is installed ---------------------------------------- #

# Check if Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v ansible &> /dev/null
then
    echo "Ansible is not installed. Please install it first."
    exit 1
fi

# ------------------------------------- Parse command-line arguments ------------------------------------------------ #

# Initialize variables
destroy=false
reconfigure=false
destroy_build=false
configure_only=false

# Parse command-line arguments
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -d|--destroy)
        destroy=true
        ;;
        -r|--reconfigure)
        reconfigure=true
        ;;
        -db|--destroy_build)
        destroy_build=true
        ;;
        -c|--configure)
        configure_only=true
        ;;
        *)
        echo "Invalid argument: $1"
        help
        exit 1
        ;;
    esac

    shift
done

# ------------------------------------- Terraform actions ----------------------------------------------------------- #
# If configure_only flag is set, only configure the private cloud environment
if ! $configure_only
then
    # If destroy flag is set, destroy the private cloud environment
    if $destroy
    then
        # terraform destroy -auto-approve
        echo "Destroying the private cloud environment"
        exit 1
    fi

    # If reconfigure flag is set, run "terraform init -reconfigure", otherwise just run "terraform init"
    if $reconfigure
    then
        terraform init -reconfigure
    else
        terraform init
    fi

    # If destroy_build flag is set, destroy the private cloud environment and then build it
    if $destroy_build
    then
        terraform destroy -auto-approve
        terraform init -reconfigure
    fi

    terraform apply -auto-approve
    sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
    terraform output -json > private_env_terraform_output.json
fi

# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.control_plane_ip.value[0]' terraform_output.json)
worker_ips=$(jq -r '.worker_ips.value | join(" ")' terraform_output.json)
management_node_public_ip=$(jq -r '.management_node_public_ip.value' terraform_output.json)

print_info "Management node floating IP: $management_node_floating_ip"

# ------------------------------------ Configuring the private cloud ------------------------------------------------ #



# Write the Ansible hosts file
cat > hosts << EOF
[control_plane]
$control_plane_ip 

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip" >> hosts
done

# Add the Ansible variables to the hosts file
cat >> hosts << EOF

[control_plane:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

[workers:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

EOF

# Copy the Ansible hosts file, terraform output and kube_cluster files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr hosts terraform_output.json ../../kube_cluster/ scripts/configure_management_node.sh ubuntu@$management_node_public_ip:~/ansible
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/.ssh/id_spotkube.pub ~/.ssh/id_spotkube ubuntu@$management_node_public_ip:~/.ssh

# Connect to the remote server
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF

cd ansible
sh configure_management_node.sh
cp kube_cluster/.ansible.cfg ~/.ansible.cfg
ansible-playbook -i hosts kube_cluster/initial.yml
ansible-playbook -i hosts kube_cluster/kube-depndencies.yml
ansible-playbook -i hosts kube_cluster/control-plane.yml
EOF