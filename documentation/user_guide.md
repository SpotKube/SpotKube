# SpotKube User Guide
SpotKube is an open-source product that optimizes Kubernetes cluster management and reduces costs by leveraging spot instances. This guide provides instructions on how to clone the SpotKube repository and configure its various components.

## Cloning SpotKube
To clone the SpotKube repository, follow these steps:

1. Open a terminal window.
2. Change to the directory where you want to clone the repository.
3. Run the following command:

```
git clone https://github.com/SpotKube/SpotKube.git 
```

This will create a local copy of the SpotKube repository in the current directory.

## Configuring Components

- Configuring Load Testing

- Configuring Analytical Model

- [Configuring Provisioner](provisioner.md)

## Run SpotKube service
Before running SpotKube, make sure that you have configured all the necessary components by following the instructions provided in the previous sections.

To run SpotKube, follow these steps:

1. Navigate to the project root directory using the terminal:
```
cd /path/to/SpotKube
```

2. Execute the `run.sh` script:
```
./run.sh
```

3. Follow the prompts and choose the appropriate options based on your requirements.

That's it! Once the services are up and running, you can use the SpotKube product to deploy and manage your microservices in the cloud.

[Back to Main Readme](../README.md)
