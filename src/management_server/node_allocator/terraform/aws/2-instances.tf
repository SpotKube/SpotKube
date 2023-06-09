resource "aws_instance" "master_node" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  key_name      = aws_key_pair.key.key_name

  subnet_id              = aws_subnet.spot_private_subnet.id
  vpc_security_group_ids = ["${data.terraform_remote_state.env_setup.outputs.security_group_ssh_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_http_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_https_id}", aws_security_group.ingress_kubeapi.id]

  tags = {
    "Name" : "spotkube_master_node"
  }
}

resource "aws_instance" "worker_node" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  key_name      = aws_key_pair.key.key_name

  subnet_id              = aws_subnet.spot_private_subnet.id
  vpc_security_group_ids = ["${data.terraform_remote_state.env_setup.outputs.security_group_ssh_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_http_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_https_id}", aws_security_group.ingress_kubeapi.id, aws_security_group.ingress_prometheus.id]

  tags = {
    "Name" : "spotkube_worker_node"
  }
}

resource "aws_eip" "worker_node-eip" {
  instance = aws_instance.worker_node.id
  vpc      = true
}
