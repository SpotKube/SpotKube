#! /bin/bash
set -e

source "../../../common/scripts/common_pkg_installer.sh"

# Create ansible config file
touch ~/.ansible.cfg
echo "[defaults]" >> ~/.ansible.cfg
echo "host_key_checking = False" >> ~/.ansible.cfg
