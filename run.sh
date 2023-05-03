#!/bin/bash

source src/scripts/common.sh

print_title "Welcome to the Spotkube"

# ------------------------------------- Load Testing service functions --------------------------------------------- #
# Function to run Load Testing service
function run_load_testing {
    echo
    print "Running Load Testing service..."
    # insert command to run Load Testing service here
}

# ----------------------------------- Analytical Model service functions ------------------------------------------- #
# Function to run Analytical Model service
function run_analytical_model {
    echo
    print "Running Analytical Model service..."
    # insert command to run Analytical Model service here
}

# ------------------------------------- Provisioner service functions ---------------------------------------------- #

# Function to run provisioner options
function run_provisioner_options {
    echo
    print "Please choose your action:"
    print "1) Initialize"
    print "2) Configure"
    print "3) Init Reconfigure"
    print "4) Destroy"
    print "5) Destroy and Build"
    read -p "Enter your choice: " ch
    case $ch in
        4)
            ./terraform_run.sh -d
            ;;
        5)
            ./terraform_run.sh -db
            ;;
        3)
            ./terraform_run.sh -r
            ;;
        2)
            ./terraform_run.sh -c
            ;;
        1)
            ./terraform_run.sh -i
            ;;
        *)
            print_error "Invalid choice. Please try again."
            ;;
    esac
}

# Function to run Provisioner service
function run_provisioner {
    echo
    print "Running Provisioner service..."
    print "Please choose your cloud environment:"
    print "1) Private Cloud"
    print "2) AWS"
    read -p "Enter your choice: " choice
    case $choice in
        1)
            print "Running Provisioner service on Private Cloud..."
            
            pushd src/provisioner/private_cloud/terraform
            run_provisioner_options
            
            ;;
        2)
            print "Running Provisioner service on AWS..."
            
            pushd src/provisioner/aws/terraform
            run_provisioner_options

            ;;
        *)
            print_error "Invalid choice. Please try again."
            ;;
    esac
}

# ------------------------------------------- Exit script function ----------------------------------------------- #

# Function to exit the script
function exit_script {
    echo
    print "Exiting Spotkube. Goodbye!"
    exit 0
}

# ------------------------------------------- Main script -------------------------------------------------------- #
# Main loop to prompt user for service choice
while true
do
    echo
    print "Please select a service to run:"
    print "1) Load Testing"
    print "2) Analytical Model"
    print "3) Provisioner"
    print "4) Exit"
    read -p "Enter your choice: " choice
    case $choice in
        1)
            run_load_testing
            ;;
        2)
            run_analytical_model
            ;;
        3)
            run_provisioner
            ;;
        4)
            exit_script
            ;;
        *)
            echo
            print_error "Invalid choice. Please try again."
            ;;
    esac
done

