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

# Function to run Load Testing service
function run_load_testing {
    whiptail --msgbox "Running Load Testing service..." 8 40
}

# Function to run Analytical Model service
function run_analytical_model {
    whiptail --msgbox "Running Analytical Model service..." 8 40
}

# ------------------------------------- Provisioner service functions ---------------------------------------------- #

# Function to run provisioner options
function run_provisioner_options {
    while true; do
        choice=$(whiptail --title "SpotKube Provisioner Options" --menu "Please choose your action:" 12 50 7 \
            "1" "Initialize" \
            "2" "Configure" \
            "3" "Init Reconfigure" \
            "4" "Destroy" \
            "5" "Destroy and Build" \
            "6" "Back" \
            "7" "Exit" \
            3>&1 1>&2 2>&3)

        case $choice in
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
            6)
                return  # Go back to the previous menu
                ;;
            7)
                exit_script
                ;;
            *)
                whiptail --msgbox "Invalid choice. Please try again." 8 40
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
                whiptail --msgbox "Invalid choice. Please try again." 8 40
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
    choice=$(whiptail --title "SpotKube Menu" --menu --nocancel "Please select a service to run:" --backtitle "Check" 12 50 4 \
        "1" "Load Testing" \
        "2" "Analytical Model" \
        "3" "Provisioner" \
        "4" "Exit" \
        3>&1 1>&2 2>&3)

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
            whiptail --msgbox "Invalid choice. Please try again." 8 40
            ;;
    esac
done
