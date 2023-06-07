#! /bin/bash
set -o errexit

# Import common functions
source ../../../scripts/common.sh

# Help function
function help() {
    print_info "Usage:"
    echo "  -i, --init                          Initialize the private cloud environment"
    echo "  -d, --destroy                       Destroy the private cloud environment"
    echo "  -db, --destroy_build                Destroy and build the private cloud environment"
    echo "  -r, --init_reconfigure              Reconfigure the private cloud environment"
    echo "  -c, --configure                     Configure the private cloud environment"
}

# --------------------------------------------------- Logging ------------------------------------------------------- #
# Set the provisioner log file path
LOG_FILE="private_provisioner.log"


# Redirect stdout to the log file
exec 3>&1 1> >(tee >(sed 's/\x1B\[[0-9;]*[JKmsu]//g' >>"${LOG_FILE}") >&3) 2>&1

# Set the trap to log the date and time of each command
trap "date -Is" DEBUG

echo
print_title "Provisioning private cloud environment"

# ------------------------------------- Check if required files exists ---------------------------------------------- #
CONF_FILE_ERROR=false

# Check if provisioner.conf exists
if [[ ! -f ~/.config/spotkube/provisioner.conf ]]; then
    print_error "provisioner.conf does not exist"
    CONF_FILE_ERROR=true
    exit 1
else
    source ~/.config/spotkube/provisioner.conf
fi

# Check if PRIVATE_INSTANCE_SSH_KEY_PATH is set and exists
if [[ -z "$PRIVATE_INSTANCE_SSH_KEY_PATH" ]]; then
    print_error "PRIVATE_INSTANCE_SSH_KEY_PATH is not set in provisioner.conf"
    CONF_FILE_ERROR=true
elif [[ ! -f "$PRIVATE_INSTANCE_SSH_KEY_PATH" ]]; then
    print_error "PRIVATE_INSTANCE_SSH_KEY_PATH ($PRIVATE_INSTANCE_SSH_KEY_PATH) does not exist"
    CONF_FILE_ERROR=true
fi

# Check if PRIVATE_HOST_IP is set
if [[ -z "$PRIVATE_HOST_IP" ]]; then
    print_error "PRIVATE_HOST_IP is not set in provisioner.conf"
    CONF_FILE_ERROR=true
fi

# Check if PRIVATE_HOST_USER is set
if [[ -z "$PRIVATE_HOST_USER" ]]; then
    print_error "PRIVATE_HOST_USER is not set in provisioner.conf"
    CONF_FILE_ERROR=true
fi

# Check if PRIVATE_HOST_SSH_KEY_PATH is set and exists
if [[ -z "$PRIVATE_HOST_SSH_KEY_PATH" ]]; then
    print_error "PRIVATE_HOST_SSH_KEY_PATH is not set in provisioner.conf"
    CONF_FILE_ERROR=true
elif [[ ! -f "$PRIVATE_HOST_SSH_KEY_PATH" ]]; then
    print_error "PRIVATE_HOST_SSH_KEY_PATH ($PRIVATE_HOST_SSH_KEY_PATH) does not exist"
    CONF_FILE_ERROR=true
fi

# Check if OPENSTACK_CLOUD_YAML_PATH is set and exists
if [[ -z "$OPENSTACK_CLOUD_YAML_PATH" ]]; then
    print_error "OPENSTACK_CLOUD_YAML_PATH is not set in provisioner.conf"
    CONF_FILE_ERROR=true
elif [[ ! -f "$OPENSTACK_CLOUD_YAML_PATH" ]]; then
    print_error "OPENSTACK_CLOUD_YAML_PATH ($OPENSTACK_CLOUD_YAML_PATH) does not exist"
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
print_info "Management node floating IP: $management_node_floating_ip"

# Get private instance SSH key name

# Use the 'basename' command to get the filename without the directory path
PRIVATE_INSTANCE_SSH_KEY_NAME=$(basename "$PRIVATE_INSTANCE_SSH_KEY_PATH")

# Print the value of PRIVATE_INSTANCE_SSH_KEY_NAME
print_error "PRIVATE_INSTANCE_SSH_KEY_NAME: $PRIVATE_INSTANCE_SSH_KEY_NAME"

# ------------------------------------ Configuring the private cloud ------------------------------------------------ #
<<COMMENT
Due to a limitation in the security rules of the private cloud that prevents the configuration file from being 
sent directly to the management node. As a workaround, the file is first sent to the host and then forwarded to the 
management node.
COMMENT

# Copy required files to the private host
print_info "Coping required files to the private host"

# Connect to the remote server
# ssh -o StrictHostKeyChecking=no -i $PRIVATE_HOST_SSH_KEY_PATH $PRIVATE_HOST_USER@$PRIVATE_HOST_IP <<EOF
# if [ ! -d "/home/spotkube/.config/spotkube" ]; then
#     mkdir -p /home/spotkube/.config/spotkube
# fi
# if [ ! -d "/home/spotkube/.ssh" ]; then
#     mkdir -p /home/spotkube/.ssh
# fi
# if [ ! -d "/home/spotkube/helm_charts" ]; then
#     mkdir -p /home/helm_charts
# fi
# EOF

# # scp -o StrictHostKeyChecking=no -i $PRIVATE_HOST_SSH_KEY_PATH -vr \
# # "$PRIVATE_INSTANCE_SSH_KEY_PATH" "$PRIVATE_INSTANCE_SSH_KEY_PATH.pub" $PRIVATE_HOST_USER@$PRIVATE_HOST_IP:~/.ssh

# scp -o StrictHostKeyChecking=no -i $PRIVATE_HOST_SSH_KEY_PATH -vr ./scripts/configure_private_management_node.sh \
# "$OPENSTACK_CLOUD_YAML_PATH" $AWS_SHARED_CONFIG_FILE_PATH $AWS_SHARED_CREDENTIALS_FILE_PATH ~/.config/spotkube/ \
# $PRIVATE_HOST_USER@$PRIVATE_HOST_IP:~/

# print_info "Copied1"

# # ------- Copying helm charts to the private host ------- #
# # Read helm chart paths from user_config.yml

# print_info "Copying helm charts to the private host"

# HELM_CHARTS=()
# while IFS= read -r line
# do
#     if [[ "$line" == *"helmChartPath"* ]]; then
#         chart_path=$(echo "$line" | cut -d: -f2- | tr -d '[:space:]' | tr -d '"' | tr -d ',')
#         if [[ -d "$chart_path" ]]; then
#             HELM_CHARTS+=("$chart_path")
#         fi
#     fi
#     echo "$line"
#     echo "chart_path: $chart_path"
# done < ~/.config/spotkube/user_config.yml

# # Print out the list of helm chart paths
# echo "HELM_CHARTS: ${HELM_CHARTS[@]}"

# # Copy helm charts to remote server
# for chart in "${HELM_CHARTS[@]}"
# do
#     echo "Copying $chart to $PRIVATE_HOST_USER@$PRIVATE_HOST_IP"
#     scp -o StrictHostKeyChecking=no -i "$PRIVATE_HOST_SSH_KEY_PATH" -vr "$chart" "$PRIVATE_HOST_USER@$PRIVATE_HOST_IP":~/helm_charts/
# done

# SSH to the private host and then ssh to the management node and run the configure_management_node.sh script
ssh -o StrictHostKeyChecking=no -i "$PRIVATE_HOST_SSH_KEY_PATH" -T $PRIVATE_HOST_USER@$PRIVATE_HOST_IP <<EOF

# mkdir -p ~/management_node
# mv ~/configure_private_management_node.sh ~/management_node/

# # copy configure_management_node.sh to the management node
# echo "Coping required files to the management node"

# scp -o StrictHostKeyChecking=no -i "~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME" -vr ~/config ~/credentials \
# ~/management_node/configure_private_management_node.sh ~/clouds.yaml ~/spotkube/ ~/helm_charts/ \
# $PRIVATE_INSTANCE_USER@$management_node_floating_ip:~/

# scp -o StrictHostKeyChecking=no -i "~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME" -vr \
# "~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME" $PRIVATE_INSTANCE_USER@$management_node_floating_ip:~/.ssh

# scp -o StrictHostKeyChecking=no -i "~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME" -vr \
# $PRIVATE_HOST_USER@$PRIVATE_HOST_IP:"~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME.pub" $PRIVATE_INSTANCE_USER@$management_node_floating_ip:~/.ssh

ssh -o StrictHostKeyChecking=no -i "~/.ssh/$PRIVATE_INSTANCE_SSH_KEY_NAME" -T $PRIVATE_INSTANCE_USER@$management_node_floating_ip <<FED1
sudo sed -i '1i127.0.0.1 private-management' /etc/hosts

touch ~/resolv.conf
echo "nameserver 8.8.8.8" > ~/resolv.conf
sudo cp ~/resolv.conf /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
sudo /etc/init.d/networking restart

mkdir -p ~/scripts
mv ~/configure_private_management_node.sh ~/scripts/

sh ~/scripts/configure_private_management_node.sh
echo "Configure management node done"

if [ ! -d "/home/ubuntu/.config/spotKube" ]; then
    mkdir -p /home/ubuntu/.config/spotKube
fi
if [ ! -d "/home/ubuntu/SpotKube" ]; then
    git clone https://github.com/SpotKube/SpotKube.git
fi

mv /home/ubuntu/spotkube /home/ubuntu/.config/spotKube/

FED1
EOF
