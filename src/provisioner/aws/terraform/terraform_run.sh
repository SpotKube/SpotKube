#! /bin/bash

# Import common functions
source ../../../scripts/common.sh

set -o errexit

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
LOG_FILE="../../../../logs/public_provisioner.log"


# Redirect stdout to the log file
exec 3>&1 1> >(tee >(sed 's/\x1B\[[0-9;]*[JKmsu]//g' >>"${LOG_FILE}") >&3) 2>&1

# Set the trap to log the date and time of each command
trap "date -Is" DEBUG

echo
print_title "Provisioning public cloud environment"

# ------------------------------------- Check if required files exists ---------------------------------------------- #
CONF_FILE_ERROR=false

# Check if provisioner.conf exists
if [[ ! -f "$HOME/.config/spotkube/provisioner.conf" ]]; then
    print_error "provisioner.conf does not exist"
    CONF_FILE_ERROR=true
    exit 1
else
    source "$HOME/.config/spotkube/provisioner.conf"
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
if [[ ! -f "$PUBLIC_INSTANCE_SSH_KEY_PATH" ]]; then
    print_error "PUBLIC_INSTANCE_SSH_KEY_PATH ($AWS_SHARED_CREDENTIALS_FILE_PATH) does not exist"
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
        -h|--help)
        help
        exit 0
        ;;
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
# If configure_only flag is set, only configure the public cloud environment
if ! $configure_only
then
    # If destroy flag is set, destroy the public cloud environment
    if $destroy
    then
        # terraform destroy -auto-approve
        echo "Destroying the public cloud environment"
        terraform destroy -auto-approve -var "aws_shared_config_file_path=$AWS_SHARED_CONFIG_FILE_PATH" -var "aws_shared_credentials_file_path=$AWS_SHARED_CREDENTIALS_FILE_PATH" -var "pub_id_file_path=$PUBLIC_INSTANCE_SSH_KEY_PATH"
        exit 1
    fi

    # If reconfigure flag is set and destroy_build is not set, run "terraform init -reconfigure", otherwise just run "terraform init"
    if $reconfigure 
    then
        terraform init -reconfigure
    else
        terraform init
    fi

    # If destroy_build flag is set, destroy the public cloud environment and then build it
    if $destroy_build
    then
        terraform destroy -auto-approve -var "aws_shared_config_file_path=$AWS_SHARED_CONFIG_FILE_PATH" -var "aws_shared_credentials_file_path=$AWS_SHARED_CREDENTIALS_FILE_PATH" -var "pub_id_file_path=$PUBLIC_INSTANCE_SSH_KEY_PATH"
        terraform init -reconfigure
    elif $initialize
    then
        terraform init
    fi

    terraform apply -auto-approve -var "aws_shared_config_file_path=$AWS_SHARED_CONFIG_FILE_PATH" -var "aws_shared_credentials_file_path=$AWS_SHARED_CREDENTIALS_FILE_PATH" -var "pub_id_file_path=$PUBLIC_INSTANCE_SSH_KEY_PATH"
    sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
fi

terraform output -json > public_env_terraform_output.json

# Read control_plane_ip and worker_ips from input.json using jq
management_node_public_ip=$(jq -r '.management_node_public_ip.value' public_env_terraform_output.json)

print_info "AWS Management node public IP: $management_node_public_ip"

# ------------------------------------ Configuring the public cloud ------------------------------------------------ #

# ------- Copying helm charts to the private host ------- #
# Read helm chart paths from user_config.yml

# Connect to the remote server
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF
if [ ! -d "/home/ubuntu/.config/spotkube" ]; then
    mkdir -p /home/ubuntu/.config/spotkube
fi
if [ ! -d "/home/ubuntu/.ssh" ]; then
    mkdir -p /home/ubuntu/.ssh
fi
if [ ! -d "/home/ubuntu/SpotKube" ]; then
    git clone https://github.com/SpotKube/SpotKube.git
fi
if [ ! -d "/home/ubuntu/helm_charts" ]; then
    mkdir -p /home/ubuntu/helm_charts
fi
EOF

HELM_CHARTS=()
while IFS= read -r line
do
    if [[ "$line" == *"helmChartPath"* ]]; then
        chart_path=$(echo "$line" | cut -d: -f2- | tr -d '[:space:]' | tr -d '"' | tr -d ',')
        if [[ -d "$chart_path" ]]; then
            HELM_CHARTS+=("$chart_path")
        fi
    fi
done < ~/.config/spotkube/user_config.yml

# Print out the list of helm chart paths
echo "HELM_CHARTS: ${HELM_CHARTS[@]}"

# Copy helm charts to remote server
for chart in "${HELM_CHARTS[@]}"
do
    scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr "$chart" "ubuntu@$management_node_public_ip":~/helm_charts/
done

echo "Helm charts copied to the remote server"

echo $HOME

# Copy the Ansible hosts file, terraform output and kube_cluster files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -r $HOME/.config/spotkube ubuntu@$management_node_public_ip:~/.config/
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr $HOME/.ssh/id_spotkube.pub ~/.ssh/id_spotkube ubuntu@$management_node_public_ip:~/.ssh
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr public_env_terraform_output.json ubuntu@$management_node_public_ip:~/SpotKube/src/provisioner/aws/terraform/

# Connect to the remote server
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF
cd SpotKube/src/provisioner/aws/terraform/scripts
chmod +x configure_management_node.sh
./configure_management_node.sh
EOF

# Copy the aws shared config and credentials files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr $AWS_SHARED_CONFIG_FILE_PATH ubuntu@$management_node_public_ip:~/.aws/config
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr $AWS_SHARED_CREDENTIALS_FILE_PATH ubuntu@$management_node_public_ip:~/.aws/credentials

echo "AWS cloud configuration done"
