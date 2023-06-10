#!/bin/bash

set -e

# Import the common functions
source ../../scripts/common.sh

# This script is used to setup the environment for the elastic scalar
print_title "Setting up the environment for the elastic scalar"

cd ../

# Install go dependecies
print_info "Installing go dependencies"
go mod download

# Compile the elastic scalar
print_info "Compiling the elastic scalar"
# Make sure the bin directory exists
mkdir -p ./bin
cd ./cmd/server
go build -o ../../bin/elastic_scalar

print_success "Successfully setup the environment for the elastic scalar"