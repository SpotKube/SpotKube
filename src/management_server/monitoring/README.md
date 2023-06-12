# Setup monitoring
This directory contains the instructions to setup monitoring for the cluster.
To monitor the cluster, we will use [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/).
Additionly we install necessary tools to monitor the cluster.
- Metrics server
- Node exporter
- Cadvisor [under testing]

## Prerequisites
- Provision the environment using the [provisioner](../../provisioner/README.md).
- Configure the cluster using the [node_allocator](../node_allocator/README.md).

## Run setup
```shell
./setup.sh
```