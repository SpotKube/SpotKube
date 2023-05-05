# User Configs

The `user_config.yml` is a configuration file that defines the parameters for your microservices named private resources.

## Microservice Properties

Each microservice has the following properties:

- name: A string that specifies the name of the service.
- minRPS: An integer that specifies the minimum requests per second that the service can handle.
- maxRPS: An integer that specifies the maximum requests per second that the service can handle.
- private: A boolean that specifies whether the service is private or not. If the service is private, it means that it can only be accessed by - other services within the same private network.
- helmChartPath: A string that specifies the path to the Helm chart for the service.

## Private Resources

The `privateResources` section defines the private resources that are available for the microservices. It includes the following properties:

- nodeCount: An integer that specifies the number of nodes available for the private network.
- nodeCPU: An integer that specifies the number of CPUs available for each node.
- nodeMemory: An integer that specifies the amount of memory available for each node.

## Sample file format

```
version: 1.0

services:
  - name: service1
    maxRPS: 10000
    minRPS: 100
    private: True
    helmChartPath: "/home/<user>/projects/fyp/microservices/microservices-python/src/auth/auth-chart"

  - name: service2
    maxRPS: 50000
    minRPS: 100
    private: True
    helmChartPath: "/home/<user>/projects/fyp/microservices/microservices-python/src/converter/converter-chart"

  - name: service3
    maxRPS: 50000
    minRPS: 100
    private: False
    helmChartPath: "/home/<user>/projects/fyp/microservices/microservices-python/src/converter/public-chart"

privateResources:
      nodeCount: 10
      nodeCPU: 4
      nodeMemory: 8

```