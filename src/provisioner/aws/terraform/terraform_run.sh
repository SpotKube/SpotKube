#! /bin/bash

# Import common functions
source ../../../scripts/common.sh

# ------------------------------------------------ Help function ---------------------------------------------------- #

function help() {
    print_info "Usage:"
    echo "  -i, --init                          Initialize the aws cloud environment"
    echo "  -d, --destroy                       Destroy the aws cloud environment"
    echo "  -db, --destroy_build                Destroy and build the aws cloud environment"
    echo "  -r, --init_reconfigure                   Reconfigure the aws cloud environment"
    echo "  -c, --configure                     Configure the aws cloud environment"
}

# --------------------------------------------------- Logging ------------------------------------------------------- #
# Set the provisioner log file path
LOG_FILE="aws_provisioner.log"


# Redirect stdout to the log file
exec 3>&1 1> >(tee >(sed 's/\x1B\[[0-9;]*[JKmsu]//g' >>"${LOG_FILE}") >&3) 2>&1

# Set the trap to log the date and time of each command
trap "date -Is" DEBUG

echo
print_title "Provisioning public cloud environment"

# ------------------------------------- Check if required files exists ---------------------------------------------- #
CONF_FILE_ERROR=false

# Check if provisioner.conf exists
if [[ ! -f "~/.config/spotkube/provisioner.conf" ]]; then
    print_error "provisioner.conf does not exist"
    CONF_FILE_ERROR=true
    exit 1
else
    source "~/.config/spotkube/provisioner.conf"
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

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "Jq is not installed. Please install it first."
    exit 1
fi

# ------------------------------------- Parse command-line arguments ------------------------------------------------ #

# Initialize variables
destroy=false
reconfigure=false
destroy_build=false
configure_only=false
initialize=false

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
        -i|--init)
        initialize=true
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
        terraform destroy -auto-approve
        echo "Destroying the private cloud environment"
        exit 1
    fi

    # If reconfigure flag is set and destroy_build is not set, run "terraform init -reconfigure", otherwise just run "terraform init"
    if $reconfigure 
    then
        terraform init -reconfigure
    elif $destroy_build
    then
        terraform destroy -auto-approve
        terraform init -reconfigure
    elif $initialize
    then
        terraform init
    fi

    terraform apply -auto-approve
    sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
    terraform output -json > private_env_terraform_output.json
fi

# Read the management node floating IP from terraform output
management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' private_env_terraform_output.json)

print_info "AWS Management node public IP: $management_node_public_ip"

# ------------------------------------ Configuring the public cloud ------------------------------------------------ #

# Copy the Ansible hosts file, terraform output and kube_cluster files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr scripts/configure_management_node.sh ubuntu@$management_node_public_ip:~/
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/.ssh/id_spotkube.pub ~/.ssh/id_spotkube ubuntu@$management_node_public_ip:~/.ssh

# Connect to the remote server
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF
sh configure_management_node.sh
EOF

# Copy the aws shared config and credentials files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr $AWS_SHARED_CONFIG_FILE_PATH ubuntu@$management_node_public_ip:~/.aws/config
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr $AWS_SHARED_CREDENTIALS_FILE_PATH ubuntu@$management_node_public_ip:~/.aws/credentials
