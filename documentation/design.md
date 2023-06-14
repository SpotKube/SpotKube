[Back to Main Readme](../README.md)

## High Level Architecture

<p align="center">
  <img src="design/hl_a3.png" width="600">
</p>


## Provisioner Component

The Provisioner component is a critical part of the system that creates the necessary environment in both public and private cloud environments. This environment is used to deploy microservice applications and run various services such as the optimization engine, node allocator, and helm service.

<p align="center">
  <!-- <img src="documentation/images/hl_a3.png" width="600"> -->
  <img src="design/provisioner.png"  width="600">
</p>

- **VPC** - A virtual private cloud (VPC) is utilized to create a private cloud computing environment within the public cloud. This VPC provides a secure and isolated network environment for deploying microservices, ensuring the confidentiality and integrity of our applications.

- **VPC NAT gateway** - Within the VPC, a NAT gateway service is employed to enable instances in a private subnet to connect to the internet. Traffic is routed from the NAT gateway to the internet gateway, and an Elastic IP is associated with the NAT gateway. This allows the instances to communicate with the internet using the IP address of the NAT gateway, providing secure outbound internet access for our microservice applications.

- **Internet gateway** - An internet gateway is used to enable resources in the public subnet to connect to the internet. This allows for communication between the management node, application, and the internet as needed \cite{Connectt63:online}. 

- **Management node** -  The management node is assigned an Elastic IP to make it accessible from the internet. Spotkube services, such as the optimization engine, node allocator, and helm service, run on this management node, providing the necessary functionalities for managing and optimizing the microservice application deployment process.

- **Master node** - The master node is responsible for cluster management and provides the API that is used to configure and manage resources within the Kubernetes cluster. This ensures efficient management of microservices and their resources within the deployed environment. 

## Node Allocator Component

<p align="center">
  <img src="design/node_allocator.png"  width="600">
</p>

The optimization engine calculates the optimal combination of nodes to deploy the microservice application and returns two terraform variable definition files for the public cloud and private cloud and triggers the node allocator.

Then using the predicted spot price in the variable definition file, the node allocator requests spot instances from the spot market and assign them to the private subnet in the virtual private cloud inside the public cloud and using the variable definition file for the private cloud, creates virtual instances in the private cloud using OpenStack with terraform. 

Once the spot instances and private cloud virtual instances are acquired, the node allocator proceeds to configure the master node and other worker nodes, these worker nodes are then assigned to the private and public clusters. Finally, the node allocator triggers the helm service to deploy the microservices with the initial optimal replica count calculated from the analytical model in the cluster.