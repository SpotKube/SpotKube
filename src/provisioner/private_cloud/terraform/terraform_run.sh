#! /bin/bash

# Import common functions
source ../../../scripts/common.sh
source "../../../../.config/provisioner.conf"

# Help function
function help() {
    print_info "Usage:"
    echo "  -d, --destroy                       Destroy the private cloud environment"
    echo "  -db, --destroy_build                Destroy and build the private cloud environment"
    echo "  -r, --reconfigure                   Reconfigure the private cloud environment"
    echo "  -c, --configure                     Configure the private cloud environment"
}

print_title "Provisioning private cloud environment"

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

# Read the management node floating IP from terraform output
management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' private_env_terraform_output.json)
print_info "Management node floating IP: $management_node_floating_ip"

# ------------------------------------ Configuring the private cloud ------------------------------------------------ #
<<COMMENT
Due to a limitation in the security rules of the private cloud that prevents the configuration file from being 
sent directly to the management node. As a workaround, the file is first sent to the host and then forwarded to the 
management node.
COMMENT

# Copy required files to the private host
scp -o StrictHostKeyChecking=no -i $PRIVATE_HOST_SSH_KEY_PATH -vr $PRIVATE_INSTANCE_SSH_KEY_PATH $PRIVATE_HOST_USER@$PRIVATE_HOST_IP:~/.ssh/
scp -o StrictHostKeyChecking=no -i $PRIVATE_HOST_SSH_KEY_PATH -vr ./scripts/configure_private_management_node.sh $PRIVATE_HOST_USER@$PRIVATE_HOST_IP:~/

# SSH to the private host and then ssh to the management node and run the configure_management_node.sh script
ssh -o StrictHostKeyChecking=no -i "$PRIVATE_HOST_SSH_KEY_PATH" -T $PRIVATE_HOST_USER@$PRIVATE_HOST_IP <<EOF

mkdir ~/management_node
mv ~/configure_private_management_node.sh ~/management_node/

# copy configure_management_node.sh to the management node
scp -o StrictHostKeyChecking=no -i $PRIVATE_INSTANCE_SSH_KEY_PATH -vr ~/management_node/configure_private_management_node.sh $PRIVATE_INSTANCE_USER@$management_node_floating_ip:~/

ssh -o StrictHostKeyChecking=no -i "$PRIVATE_INSTANCE_SSH_KEY_PATH" -T $PRIVATE_INSTANCE_USER@$management_node_floating_ip <<FED1
sudo sed -i '1i127.0.0.1 private-management' /etc/hosts

mkdir ~/scripts
mv ~/configure_private_management_node.sh ~/scripts/
sh ~/scripts/configure_private_management_node.sh

# Generate new SSH key for ansible to use
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa

echo "Configure management node done"
touch ~/management_node_done.txt

FED1
EOF



