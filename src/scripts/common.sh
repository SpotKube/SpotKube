#!/bin/bash

# Function to echo colored warnning messages
function print_warn() {
    echo -e "\033[1;33mWARN: $1\033[0m"
}

# Function to echo colored error messages
function print_error() {
    echo -e "\033[1;31mERROR: $1\033[0m"
}

# Function to echo colored success messages
function print_success() {
    echo -e "\033[1;32mSUCCESS: $1\033[0m"
}

# Function to echo colored info messages
function print_info() {
    echo -e "\033[1;34mINFO: $1\033[0m"
}

# Function to echo blue color large text
function print_title() {
    echo -e "\033[1;36m$1\033[0m"
}
