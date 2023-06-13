#!/bin/bash

set -e

# Import the helper functions
source ../../../scripts/common.sh

# Setup prometheus
function setup_prometheus() {
    # Install prometheus
    print_info "Installing prometheus"

    kubectl apply -f ../prom/namespace.yaml
    kubectl apply -f ../prom/clusterRole.yaml
    kubectl apply -f ../prom/config-map.yaml
    kubectl apply -f ../prom/prometheus-deployment.yaml
    kubectl apply -f ../prom/prometheus-service.yaml

    print_success "Prometheus installed successfully. Sleeping for 30s..."
    sleep 30
}

function install_adons() {
    # Install addons
    print_info "Installing addons"

    kubectl apply -f ../addons/metrics_server.yaml

    print_success "Addons installed successfully. Sleeping for 30s..."
    sleep 30
}

function install_scrapers() {
    # Install scrapers
    print_info "Installing scrapers"

    kubectl apply -f ../scrapers/node_exporter_ds.yaml
    kubectl apply -f ../scrapers/node_exporter_svc.yaml

    print_success "Scrapers installed successfully. Sleeping for 30s..."
    sleep 30
}

function setup_grafana() {
    # Install grafana
    print_info "Installing grafana"

    kubectl apply -f ../grafana/configMap.yaml
    kubectl apply -f ../grafana/deployment.yaml
    kubectl apply -f ../grafana/service.yaml

    print_success "Grafana installed successfully. Sleeping for 30s..."
    sleep 30
}

print_title "Setting up monitoring"

setup_prometheus
install_adons
install_scrapers
setup_grafana

print_success "Monitoring setup successfully"