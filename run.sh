#!/bin/bash

export DIALOG_BACKTITLE="Spotkube - Interactive Menu"

export NEWT_COLORS='
root=,blue
window=,black
shadow=,blue
border=blue,black
title=red,black
textbox=blue,black
button=black,white
label=black,blue
compactbutton=black,white
checkbox=black,blue
radiobox=black,blue
radiolist=black,blue
actlist=black,blue
msgbox=black,blue
'
timeout=2

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


# ----------------------------------------- Load Testing Service ----------------------------------------------- #
# Function to run Load Testing service
function run_load_testing {
    whiptail --msgbox "Running Load Testing service..." 8 40
}


# ----------------------------------------- Analytical Model Service ----------------------------------------------- #

# Function to run Analytical Model service
function run_analytical_model {
    whiptail --msgbox "Running Analytical Model service..." 8 40
}

# ------------------------------------ Managemenet Server service functions ----------------------------------------- #

function run_mgt_server_options() {
    local cloud="$1"
    local mgt_server_url=""
    local startup_url=""
    local destroy_url=""

    if [ "$cloud" == "private" ]; then
        pushd src/provisioner/private_cloud/terraform 
        # Read the management node floating IP from terraform output
        management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' private_env_terraform_output.json)
        startup_url="http://$management_node_floating_ip/startup_private_cloud"
        destroy_url="http://$management_node_floating_ip/node_allocator/private/destroy"
        popd

    elif [ "$cloud" == "aws" ]; then
        pushd src/provisioner/aws/terraform 
        # Read control_plane_ip and worker_ips from input.json using jq
        management_node_public_ip=$(jq -r '.management_node_public_ip.value' public_env_terraform_output.json)
        startup_url="http://$management_node_public_ip/startup_aws_cloud"
        destroy_url="http://$management_node_public_ip/node_allocator/aws/destroy"
        popd
    fi

    while true; do
        choice=$(whiptail --nocancel --title "SpotKube Management Server Options" --menu "Please choose your action:" 12 50 4 \
            "1" "Configure and Deploy" \
            "2" "Destroy Cloud" \
            "3" "Back" \
            "4" "Exit" \
            3>&1 1>&2 2>&3)

        case $choice in
            1)
                output=$(curl --location --max-time $timeout "$startup_url" 2>&1)
                exit_code=$?
                if [ $exit_code -eq 0 ]; then
                    echo "$output"
                    whiptail --title "Result" --msgbox "Configured and Deployed Successfully." 8 40
                else
                    echo "$output"
                    whiptail --title "Error" --msgbox "Error occurred. Exit code: $exit_code"  8 40 
                fi
                ;;                
            2)
                output=$(curl --location --max-time $timeout "$destroy_url" 2>&1)
                exit_code=$?
                if [ $exit_code -eq 0 ]; then
                    echo "$output"
                    whiptail --title "Result" --msgbox "Destroyed Successfully." 8 40
                else
                    echo "$output"
                    whiptail --title "Error" --msgbox "Error occurred. Exit code: $exit_code"  8 40 
                fi
                ;;
            3)
                return  # Go back to the previous menu
                ;;
            4)
                exit_script
                ;;
            *)
                exit_script
                ;;
        esac
    done
}

# Function to run Provisioner service
function run_mgt_server {
    while true; do
        choice=$(whiptail --title "SpotKube Management Server" --nocancel --menu "Please choose your cloud environment:" 12 50 4 \
            "1" "Private Cloud" \
            "2" "AWS" \
            "3" "Back" \
            "4" "Exit" \
            3>&1 1>&2 2>&3)

        case $choice in
            1)
                run_mgt_server_options "private"
                ;;
            2)
                run_mgt_server_options "aws"
                ;;
            3)
                return  # Go back to the previous menu
                ;;
            4)
                exit_script
                ;;
            *)
                exit_script
                ;;
        esac
    done
}

# ------------------------------------- Provisioner service functions ---------------------------------------------- #

# TODO: Fix and check if this works
run_with_whiptail() {
    local command="$1"
    local title="$2"
    local message="$3"

    # Create a temporary file to capture the command output
    local temp_file=$(mktemp)

    whiptail --msgbox "$command" 8 40
    # Run the command in the background and redirect its output to the temporary file
    "$command" >"$temp_file" 2>&1 &

    # Start a loop to read the command output from the temporary file
    {
    output=$($command 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "Process completed."
    else
        echo "Error occurred. Exit code: $exit_code"
        echo "$output"
    fi
    } | whiptail --gauge "Running terraform_run.sh -c" 6 60 0

    # Check if the user pressed the 'ESC' key
    if [ $? -eq 255 ]; then
        echo "Operation terminated by the user."
        kill %1  # Terminate the background command
        exit 0
    fi

    # Close and remove the temporary file
    rm "$temp_file"

    whiptail --msgbox "$output" 8 40
}

# Function to run provisioner options
function run_provisioner_options {
    while true; do
        choice=$(whiptail --nocancel --title "SpotKube Provisioner Options" --menu "Please choose your action:" 16 50 7 \
            "1" "Initialize" \
            "2" "Configure Only" \
            "3" "Init Reconfigure" \
            "4" "Destroy" \
            "5" "Destroy and Build" \
            "6" "Back" \
            "7" "Exit" \
            3>&1 1>&2 2>&3)

        case $choice in
            4)
                bash terraform_run.sh -d
                whiptail --title "Result" --msgbox "Destroyed Successfully." 8 40
                ;;
            5)
                bash terraform_run.sh -db
                whiptail --title "Result" --msgbox "Destroyed and Built Successfully." 8 40
                ;;
            3)
                bash terraform_run.sh -r
                whiptail --title "Result" --msgbox "Reconfigured Successfully." 8 40
                ;;
            2)
                bash terraform_run.sh -c
                whiptail --title "Result" --msgbox "Configured Successfully." 8 40
                ;;
            1)
               
                bash terraform_run.sh -i
                whiptail --title "Result" --msgbox "Initialized Successfully." 8 40
                ;;
            6)
                return  # Go back to the previous menu
                ;;
            7)
                exit_script
                ;;
            *)
                exit_script
                ;;
        esac
    done
}

# Function to run Provisioner service
function run_provisioner {
    while true; do
        choice=$(whiptail --title "SpotKube Provisioner" --nocancel --menu "Please choose your cloud environment:" 12 50 4 \
            "1" "Private Cloud" \
            "2" "AWS" \
            "3" "Back" \
            "4" "Exit" \
            3>&1 1>&2 2>&3)

        case $choice in
            1)
                pushd src/provisioner/private_cloud/terraform
                run_provisioner_options
                popd
                ;;
            2)
                pushd src/provisioner/aws/terraform
                run_provisioner_options
                popd
                ;;
            3)
                return  # Go back to the previous menu
                ;;
            4)
                exit_script
                ;;
            *)
                exit_script
                ;;
        esac
    done
}

# ------------------------------------------- Exit script function ----------------------------------------------- #

# Function to exit the script
function exit_script {
    echo
    print "Exiting Spotkube. Goodbye!"
    exit 0
}

# Main loop to prompt user for service choice
while true
do
    choice=$(whiptail --title "SpotKube Menu" --menu --nocancel "Please select a service to run:" 12 50 5 \
        "1" "Load Testing" \
        "2" "Analytical Model" \
        "3" "Cloud Environment Setup" \
        "4" "Management Server" \
        "5" "Exit" \
        3>&1 1>&2 2>&3)

    case $choice in
        1)
            # run_load_testing
            run_load_testing
            ;;
        2)
            run_analytical_model
            ;;
        3)
            run_provisioner
            ;;
        4)
            run_mgt_server
            ;;

        5)
            exit_script
            ;;
        *)
            # whiptail --msgbox "Invalid choice. Please try again." 8 40
            exit_script
            ;;
    esac
done
