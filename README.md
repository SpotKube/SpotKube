# SpotKube

<img src="https://github.com/SpotKube/SpotKube/blob/update/readme/resources/spotkube.png" width="100">

----

SpotKube is an open-source Kubernetes-managed service that optimizes
the deployment cost of microservices applications by autoscaling 
the Kubernetes cluster in a more intelligent way. The proposed system 
for deploying microservice-based applications on hybrid clouds comprises 
several components, including application characterization, analytical model, 
provisioner, optimization engine, node allocator, helm service, container orchestration tool Kubernetes, and elastic scaler.

----

## High Level Architecture

<center><img src="https://github.com/SpotKube/SpotKube/blob/update/readme/resources/OPEN%20SOURCE%20%20-%20HL_A3_cropped.png" width="800"></center>

----

## Usage

Once you have cloned SpotKube, you can start using it to optimize the deployment of your 
microservices applications on hybrid clouds. 
To use SpotKube, you need to follow these steps:

1. Characterize your application and provide CPU and memory metrics to the analytical model.
2. The analytical model analyzes the data and determines the optimal pod count for 
deploying the microservices application without violating user-defined SLOs.
3. The provisioner builds the necessary environment in both public and private 
cloud environments for deploying the microservices application and running various services.
4. The optimization engine identifies the optimal configurations for 
deploying microservices applications on hybrid clouds, 
utilizing predictive modeling and real-time data to achieve cost-effectiveness.
5. The node allocator allocates and configures the nodes and adds them to the cluster.
5. The helm service deploys the microservices application on the Kubernetes cluster, 
which handles the scheduling.
6. The elastic scaler dynamically notifies the optimization engine about the 
current configuration, enabling it to adjust the system as needed.

For more detailed instructions on how to use SpotKube, please refer to the [user guide](https://github.com/SpotKube/SpotKube).

## Contributing

We welcome contributions from the community! To contribute to SpotKube, please follow these steps:

- Fork the SpotKube repository.
- Create a new branch for your contribution.
- Make your changes and submit a pull request.
- We will review your changes and merge them if they meet our standards.
- For more detailed instructions on how to contribute to SpotKube, please refer to the [contributing guide](https://github.com/SpotKube/SpotKube).

## Licence

SpotKube is released under the Apache 2.0 license. For more information, please refer to the [license file](https://github.com/SpotKube/SpotKube/blob/dev/LICENSE).

## Contact
If you have any questions or comments about SpotKube, please contact us or open an issue on the [GitHub Issues](https://github.com/SpotKube/SpotKube/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc).


