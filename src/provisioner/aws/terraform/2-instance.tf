data "local_file" "public_key" {
  filename = var.pub_id_file_path
}

resource "aws_key_pair" "key" {
  key_name   = "spotkube_key"
  public_key = data.local_file.public_key.content
}

# Create ec2 instances on the subnets
resource "aws_instance" "management_node" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.key.key_name

  subnet_id              = aws_subnet.spot_public_subnet.id
  vpc_security_group_ids = [aws_security_group.ingress_ssh.id, aws_security_group.ingress_http.id, aws_security_group.ingress_https.id]
  # associate_public_ip_address = true

  tags = {
    "Name" : "spotkube_managment_node"
  }
}

resource "aws_eip" "management_node-eip" {
  instance = aws_instance.management_node.id
  vpc      = true
}
