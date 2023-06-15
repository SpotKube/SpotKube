#!/bin/bash

set -e

# Import common functions
source ../../../scripts/common.sh

worker_ip=$(cat ../../node_allocator/terraform/aws/aws_instance_terraform_output.json| jq -r '.worker_node_ip.value')

# Exit if worker IP is empty
if [ -z "$worker_ip" ]; then
    echo "Worker IP is empty"
    exit 1
fi

# Extract node name from worker IP
node_name=$(kubectl get nodes -o json | jq -r '.items[] | select(."metadata"."annotations"."flannel.alpha.coreos.com/public-ip"=="'$worker_ip'") | .metadata.name')

# Exit if node name is empty
if [ -z "$node_name" ]; then
    echo "Node name is empty"
    exit 1
fi

print_info "Worker Ip: $worker_ip, Node name: $node_name"

# Attach label to node
kubectl label node $node_name monitor=True --overwrite
