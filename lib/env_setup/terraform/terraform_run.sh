#! /bin/bash

terraform init
terraform apply -auto-approve
terraform output -json > terraform_output.json
