data "local_file" "public_key" {
  filename = "/home/pasindu/.ssh/id_spotkube.pub"
}

resource "aws_key_pair" "key" {
  key_name   = "spotkube"
  public_key = "${data.local_file.public_key.content}"
}

# Create ec2 instances on the subnets
resource "aws_instance" "management_node" {
  ami           = "ami-0533f2ba8a1995cf9"
  instance_type = "t2.micro"
  key_name      = "${aws_key_pair.key.key_name}"

  subnet_id                   = aws_subnet.spot_subnet.id
  vpc_security_group_ids      = [aws_security_group.ingress_ssh.id]
  associate_public_ip_address = true

  tags = {
    "Name" : "spotkube_managment_node"
  }
}