resource "aws_spot_instance_request" "worker_nodes" {
  for_each             = var.spot_instances
  ami                  = var.ami_id
  spot_price           = each.value.spot_price
  instance_type        = each.value.instance_type
  spot_type            = "one-time"
  wait_for_fulfillment = "true"
  key_name             = aws_key_pair.key.key_name

  security_groups = ["${data.terraform_remote_state.env_setup.outputs.security_group_ssh_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_http_id}", "${data.terraform_remote_state.env_setup.outputs.security_group_https_id}", aws_security_group.ingress_kubeapi.id]
  subnet_id       = aws_subnet.spot_private_subnet.id

  tags = {
    "Name" : "${each.key}"
  }
}
