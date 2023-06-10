#! /bin/bash
# set -o errexit

echo "This is testing1"
# Import common functions
source ../../../scripts/common.sh

echo "This is testing"

cp ../../../../.config/* ~/.config/spotkube

# Help function
function help() {
    print_info "Usage:"
    echo "  -i, --init                          Initialize the private cloud environment"
    echo "  -d, --destroy                       Destroy the private cloud environment"
    echo "  -db, --destroy_build                Destroy and build the private cloud environment"
    echo "  -r, --init_reconfigure              Reconfigure the private cloud environment"
    echo "  -c, --configure                     Configure the private cloud environment"
}