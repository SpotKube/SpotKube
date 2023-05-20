#!/bin/bash

set -e 

ansible-playbook -i hosts initial.yml
ansible-playbook -i hosts kube_dependencies.yml
ansible-playbook -i hosts control_plane.yml
ansible-playbook -i hosts workers.yml
ansible-playbook -i hosts setup_kubectl.yml