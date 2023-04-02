#!/bin/bash

# Function to parse YAML file and get values
function parse_yaml {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s$w$s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s\[$s\]\(.*\)$s$|\1$fs$2\[$fs\2\]$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s$|\1$fs$2$fs\2$fs\3|p"  \
        "$1" | awk -F"$fs" '{if (length($2)) {printf("%s%s=\"%s\"\n", "'$prefix'", $2, $3)}}'
}

echo "Running Helm:"

# Parse .config.yaml and loop through each service
services=$(parse_yaml ../../../.config/config.yml "services_")
for service in $services; do
  # Get helmChartPath and pod count for current service
  helmChartPath=$(echo "${services_${service}_helmChartPath}")
  podCount=$(echo "${services_${service}_minRPS_pods}")
  serviceName=$(echo "${services_${service}_name}")

  echo "Running Helm install for $serviceName with $podCount pods"

  # Run Helm chart with variable values
#   cd $helmChartPath
#   helm install auth . -f values.yaml --set replicaCount=$podCount
  helm install --set replicaCount=$podCount auth $helmChartPath
done