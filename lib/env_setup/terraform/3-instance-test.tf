# Create ec2 instances on the subnets
resource "aws_instance" "master_node" {
  ami           = "ami-0533f2ba8a1995cf9"
  instance_type = "t2.micro"
  key_name      = "${aws_key_pair.key.key_name}"

  subnet_id                   = aws_subnet.spot_subnet.id
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
  associate_public_ip_address = true

  tags = {
    "Name" : "spotkube_master_node"
  }
}

# Create ec2 instances on the subnets
resource "aws_instance" "worker_node" {
  count         = 2 
  ami           = "ami-0533f2ba8a1995cf9"
  instance_type = "t2.micro"
  key_name      = "${aws_key_pair.key.key_name}"

  subnet_id                   = aws_subnet.spot_subnet.id
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
  associate_public_ip_address = true

  tags = {
    "Name" : "spotkube_worker_node-${count.index+1}"
  }
}


# Create ec2 instances on the subnets
# resource "aws_instance" "worker_node2" {
#   ami           = "ami-0533f2ba8a1995cf9"
#   instance_type = "t2.micro"
#   key_name      = "${aws_key_pair.key.key_name}"

#   subnet_id                   = aws_subnet.spot_subnet.id
#   vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
#   associate_public_ip_address = true

#   tags = {
#     "Name" : "spotkube_test_node"
#   }
# }

# Write the public IP of the master node to a file
output "control_plane_ip" {
  value = aws_instance.master_node.*.private_ip
}


output "worker_ips" {
  value = aws_instance.worker_node.*.private_ip
}

