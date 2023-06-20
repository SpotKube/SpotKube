#!/bin/bash

ansible-playbook -i hosts initial.yml
ansible-playbook -i hosts kube_dependencies.yml
ansible-playbook -i hosts control_plane.yml
ansible-playbook -i hosts workers.yml
ansible-playbook -i hosts setup_kubectl.yml

# Remove NotReady nodes
kubectl delete node $(kubectl get nodes | grep NotReady | awk '{print $1;}')

