#!/bin/bash

# Function to echo colored warnning messages
function print_warn() {
    echo -e "\033[1;33m$1\033[0m"
}

# Function to echo colored error messages
function print_error() {
    echo -e "\033[1;31m$1\033[0m"
}

# Function to echo colored success messages
function print_success() {
    echo -e "\033[1;32m$1\033[0m"
}

# Function to echo colored info messages
function print_info() {
    echo -e "\033[1;34m$1\033[0m"
}

# Function to echo blue color large text
function print_title() {
    echo -e "\033[1;36m$1\033[0m"
}
