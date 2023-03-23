resource "aws_instance" "master_node" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  key_name      = "${aws_key_pair.key.key_name}"

  subnet_id                   = "${data.terraform_remote_state.env_setup.outputs.subnet_id}"
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]

  tags = {
    "Name" : "spotkube_master_node"
  }
}
