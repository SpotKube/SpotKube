# SpotKube

<!-- ![Builder](https://github.com/asgardeo/asgardeo-auth-react-sdk/workflows/Builder/badge.svg) -->
[![Stackoverflow](https://img.shields.io/badge/Ask%20for%20help%20on-Stackoverflow-orange)](https://stackoverflow.com/questions/tagged/spotkube)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/wso2/product-is/blob/master/LICENSE)

---


<p align="center">
  <img src="documentation/images/logo.png" width="250">
</p>

## Table of Contents

- [Introduction](#introduction)
- [Prerequisite](#prerequisite)
- [Getting Stated](#usage)
- [Architecture](#high-level-architecture)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

SpotKube is an open-source Kubernetes-managed service that optimizes the deployment cost of microservices applications 
by autoscaling the Kubernetes cluster in a more intelligent way. The system is designed to deploy microservice-based 
applications on hybrid clouds, utilizing various components such as application characterization, analytical model, 
provisioner, optimization engine, node allocator, helm service, container orchestration tool Kubernetes, and elastic 
scaler.

## Pre-requisite

- Terraform: Terraform is used to provision the necessary infrastructure in both public and private cloud environments.
- Ansible: Ansible is used to configure the provisioned infrastructure.

<!-------------------------------------------------- Getting Started  --------------------------------------------------->
## Getting Started

To start optimizing the deployment of your microservices applications on hybrid clouds using SpotKube, follow these 
steps:

### 1. Cloning SpotKube
To clone the SpotKube repository, follow these steps:

1. Open a terminal window.
2. Change to the directory where you want to clone the repository.
3. Run the following command:

```
git clone https://github.com/SpotKube/SpotKube.git 
```

This will create a local copy of the SpotKube repository in the current directory.

### 2. Configuring SpotKube

This guide provides step-by-step instructions on how to configure the SpotKube application by filling out the necessary configuration files. The configuration files include `user_config.yml`, `provisioner.conf`, `load_test.conf`, and 
`privateCost.json`.

#### User Configuration (`user_config.yml`)

The `user_config.yml` file contains user-specific configurations required for the SpotKube application. Follow the steps below to configure the `user_config.yml` file:

- Open the `user_config.yml` file in a text editor.
- Within the services section, you can define multiple services that SpotKube will manage. 
- Each service requires the following information:
  - name: The name of the service.
  - maxRPS: The maximum number of requests per second the service can handle.
  - minRPS: The minimum number of requests per second the service needs to handle.
  - private: Set this to True if the service should be deployed on private resources, or False for public resources.
  - helmChartPath: The path to the Helm chart of the service.
  -

- Optionally, you can configure the privateResources section to specify the resources for private deployments:
  - nodeCount: The number of nodes to allocate for private resources.
  - nodeCPU: The CPU resources allocated per node.
  - nodeMemory: The memory resources allocated per node.

Make sure to save the changes to the `user_config.yml` file after completing the configuration.

#### Provisioner Configuration (`provisioner.conf`)

The `provisioner.conf` file contains configuration settings for the provisioner component of SpotKube. 
Follow the steps below to configure the `provisioner.conf` file:

- Open the `provisioner.conf` file in a text editor.
- Modify the configuration parameters as required based on your cloud environment and provisioning needs. 
- Please refer to the appropriate documentation for the specific configuration options relevant to your cloud environment.
- Save the changes to the `provisioner.conf` file after completing the configuration.

```
# Private Cloud Configuration
PRIVATE_INSTANCE_SSH_KEY_PATH='/home/user/.ssh/id_spotkube'
PRIVATE_INSTANCE_USER=username
PRIVATE_HOST_IP=10.0.0.0
PRIVATE_HOST_USER=username
PRIVATE_HOST_SSH_KEY_PATH='/home/user/.ssh/id_spotkube'
OPENSTACK_CLOUD_YAML_PATH='/home/user/.config/openstack/clouds.yaml'

# Public Cloud Configuration
AWS_SHARED_CONFIG_FILE_PATH='/home/user/.aws/config'
AWS_SHARED_CREDENTIALS_FILE_PATH='/home/user/.aws/credentials'
```

The following table describes the configuration parameters in the `provisioner.conf` file:

| Parameter | Description |
| --- | --- |
| `PRIVATE_INSTANCE_SSH_KEY_PATH` | The path to the SSH key used to authenticate with private cloud instances. |
| `PRIVATE_INSTANCE_USER` | The username used to authenticate with private cloud instances. |
| `PRIVATE_HOST_IP` | The IP address of the private cloud instance that will be used as the management node. |
| `PRIVATE_HOST_USER` | The username used to authenticate with the private cloud host machine. |
| `PRIVATE_HOST_SSH_KEY_PATH` | The path to the SSH key used to authenticate with the private cloud host machine. |
| `OPENSTACK_CLOUD_YAML_PATH` | The path to the OpenStack cloud configuration file. This file contains authentication information for connecting to OpenStack clouds. |
| `AWS_SHARED_CONFIG_FILE_PATH` | The path to the AWS configuration file. This file contains configuration information for connecting to AWS services. |
| `AWS_SHARED_CREDENTIALS_FILE_PATH` | The path to the AWS credentials file. This file contains credentials for authenticating with AWS services. |

Make sure to save the changes to the `provisioner.conf` file after completing the configuration.

#### Load Test Configuration (`load_test.conf`)

The `load_test.conf` file contains configuration settings for the load testing component of SpotKube. Follow the steps below to configure the `load_test.conf` file:

- Open the `load_test.conf` file in a text editor.
- Set the `GRAFANA_API_KEY` parameter to your Grafana API key.
- Update the `GRAFANA_HOST` parameter with the URL of your Grafana instance.
- Save the changes to the `load_test.conf` file after completing the configuration.

#### Private Cost Configuration (`privateCost.json`)
The `privateCost.json` file contains cost-related configurations for private deployments in SpotKube. Follow the steps below to configure the `privateCost.json` file:

Open the `privateCost.json` file in a text editor.
Modify the values of the various cost-related parameters based on your cost structure. The parameters include:
fixedCost: Represents the fixed costs associated with private deployments, such as server cost, network device cost, software license cost, space cost, non-electric cost, Dit, Df, and Du.
variableCost: Represents the variable costs associated with private deployments, such as electricity unit cost, Eidle, Erunning, internet cost, and labor cost.
Save the changes to the `privateCost.json` file after completing the configuration.

Once you have filled out and saved the necessary configuration files (`user_config.yml`, `provisioner.conf`, `load_test.conf`, and `privateCost.json`), you can proceed to the next step.

### 3. Run SpotKube service
Before running SpotKube, make sure that you have configured all the necessary components by following the instructions 
provided in the previous sections.

To run SpotKube, follow these steps:

#### 1. Navigate to the project root directory using the terminal:
```
cd /path/to/SpotKube
```

#### 2. Execute the `run.sh` script:
```
bash run.sh
```

#### 3. Load Testing

To perform load testing with SpotKube, follow these steps:

- Select the Load Testing option from the menu.
- Provide the following inputs:
  - Name of the service to run Locust for
  - Root directory of the service
  - Host URL
  - Number of users to spawn
  - Spawn rate
  - Running time

#### 4. Analytical Model

After the load testing is completed, select the Analytical Model option from the menu. Wait for the optimal pod count 
to be calculated.

#### 5. Provisioner

- After the Analytical Model is completed, select the `Cloud Environment Setup` option from the menu. 
- Choose the cloud environment (AWS, private cloud). 
- Run the provisioner and select the `Initialize` option from the menu. 
- Wait for the environment to be initialized. You will be notified once the environment is initialized.

#### 6. Management Server
- After the Cloud Environment Setup is completed, select the `Management Server` option from the menu. 
- Choose the cloud environment (AWS, private cloud). 
- Run the management server and select the `Configure and Deploy` option from the menu. 
- Wait for microservices to be deployed. 

These management server services are available on `SpotKube Web-UI`. You can run the SpotKube Web-UI locally by running 
the following instructions in this [SpotKube Web-UI](https://github.com/SpotKube/Spotkube-UI)

For further information on using interactive cli tool, refer to the 
[SpotKube CLI tool documentation](documentation/cli.md).

That's it! Once the services are up and running, you can use the SpotKube product to deploy and manage your 
microservices in the cloud.


[Back to Table of Contents](#table-of-contents)

<!-------------------------------------------------- Architecture  --------------------------------------------------->
## Architecture

### High Level Architecture

<p align="center">
  <img src="documentation/images/design/hl_a3.png" width="600">
</p>

The high-level architecture of SpotKube is designed to optimize the deployment cost of microservices applications on 
hybrid clouds. It consists of several components working together to achieve efficient autoscaling and deployment.

### Application Characterization

Characterize your application and provide CPU and memory metrics to the analytical model.

### Analytical Model

The analytical model analyzes the data provided by the application characterization and determines the optimal pod 
count for deploying the microservices application without violating user-defined SLOs (Service Level Objectives).

### Provisioner

The provisioner is responsible for building the necessary environment in both public and private cloud environments. 
It sets up the infrastructure required for deploying the microservices application and running various services.

### Optimization Engine

The optimization engine utilizes predictive modeling and real-time data to identify the optimal configurations for 
deploying microservices applications on hybrid clouds. It aims to achieve cost-effectiveness by considering factors 
such as resource utilization, workload patterns, and cost models.

### Node Allocator

The node allocator is responsible for allocating and configuring the nodes in the cluster. It adds new nodes to the 
cluster as needed based on the workload demands and scales down the cluster when resources are underutilized.

### Helm Service

The helm service is responsible for deploying the microservices application on the Kubernetes cluster. It handles the 
scheduling and management of the application's containers.

### Elastic Scaler

The elastic scaler dynamically monitors the system's configuration and notifies the optimization engine about the 
current state. This enables the optimization engine to adjust the system's configuration in real-time, ensuring optimal 
resource utilization and cost-efficiency.

The components of SpotKube work together to optimize the deployment of microservices applications on hybrid clouds, providing scalability, cost-effectiveness, and efficient resource utilization.

For further information, refer to the [architecture documentation](documentation/design.md).

[Back to Table of Contents](#table-of-contents)

<!-------------------------------------------------- Contributing  --------------------------------------------------->
## Contributing

We welcome contributions from the community! To contribute to SpotKube, please follow these steps:

1. Fork the SpotKube repository.
2. Create a new branch for your contribution.
3. Make your changes and submit a pull request.
4. We will review your changes and merge them if they meet our standards.

For more detailed instructions on how to contribute to SpotKube, please refer to the [contributing guide](https://github.com/SpotKube/SpotKube).


[Back to Table of Contents](#table-of-contents)

<!-------------------------------------------------- License  --------------------------------------------------->
## License

SpotKube is released under the Apache 2.0 license. For more information, please refer to the [license file](https://github.com/SpotKube/SpotKube/blob/dev/LICENSE).


[Back to Table of Contents](#table-of-contents)

<!-------------------------------------------------- Contact  --------------------------------------------------->

## Contact

If you have any questions or comments about SpotKube, please contact us or open an issue on [GitHub Issues](https://github.com/SpotKube/SpotKube/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc).

[Back to Table of Contents](#table-of-contents)

