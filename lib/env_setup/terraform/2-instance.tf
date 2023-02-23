data "local_file" "public_key" {
  filename = "${var.file_path}"
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

  user_data = <<-EOF
  #!/bin/bash -ex

  sudo apt update
  sudo apt install software-properties-common
  sudo apt-add-repository --yes --update ppa:ansible/ansible
  sudo apt install ansible
  EOF

  tags = {
    "Name" : "spotkube_managment_node"
  }
}