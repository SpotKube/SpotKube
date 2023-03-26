resource "aws_vpc" "spot_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "spotkube"
  }
}

resource "aws_subnet" "spot_public_subnet" {
  # creates a subnet
  cidr_block        = cidrsubnet(aws_vpc.spot_vpc.cidr_block, 3, 1)
  vpc_id            = aws_vpc.spot_vpc.id
  availability_zone = var.availability_zone
  tags = {
    Name = "spotkube"
  }
}

# Output aws pod network cidr
output "pod_network_cidr" {
  value = aws_subnet.spot_public_subnet.cidr_block
}

# Attach an internet gateway to the VPC
resource "aws_internet_gateway" "spotkube_ig" {
  vpc_id = aws_vpc.spot_vpc.id

  tags = {
    Name = "spotkube_Internet-Gateway"
  }
}


# Create a route table for a public subnet
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.spot_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.spotkube_ig.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.spotkube_ig.id
  }

  tags = {
    Name = "Public-Route-Table"
  }
}

# Resource: aws_route_table_association
# assiociate any public subnets with the route table.
resource "aws_route_table_association" "public_1_rt_a" {
  subnet_id      = aws_subnet.spot_public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Create security groups to allow specific traffic
resource "aws_security_group" "ingress_ssh" {
  name   = "allow-ssh-sg"
  vpc_id = aws_vpc.spot_vpc.id

  ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]

    from_port = 22
    to_port   = 22
    protocol  = "tcp"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ingress_http" {
  name_prefix = "allow-http-sg"
  vpc_id = aws_vpc.spot_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "HTTP Ingress"
  }
}

resource "aws_security_group" "ingress_https" {
  name_prefix = "allow-https-sg"
  vpc_id = aws_vpc.spot_vpc.id
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "HTTPS Ingress"
  }
}
