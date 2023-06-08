#!/bin/bash

set -e

kubectl apply -f namespace.yaml
kubectl apply -f cluster_role.yaml
kubectl apply -f cluster_role_binding.yaml
kubectl apply -f config_map.yaml
kubectl apply -f deployment.yaml
# kubectl apply -f 