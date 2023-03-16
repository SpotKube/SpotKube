data "local_file" "public_key" {
  filename = "${var.pub_id_file_path}"
}

resource "aws_key_pair" "key" {
  key_name   = "spotkube_key"
  public_key = "${data.local_file.public_key.content}"
}

# Create ec2 instances on the subnets
resource "aws_instance" "management_node" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  key_name      = "${aws_key_pair.key.key_name}"

  subnet_id                   = aws_subnet.spot_subnet.id
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
  associate_public_ip_address = true

  # user_data = "${file("scripts/configure_management_node.sh")}"

  tags = {
    "Name" : "spotkube_managment_node"
  }
}

# Save the public ip of the management node
output "management_node_public_ip" {
  value = "${aws_instance.management_node.public_ip}"
}
