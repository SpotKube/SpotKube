data "terraform_remote_state" "env_setup" {
  backend = "s3"

  config = {
    bucket = "spotkube-terraform-state-bucket"
    key    = "env_setup-terraform.tfstate"
    region = "us-west-2"
  }
}

data "local_file" "public_key" {
  filename = var.pub_id_file_path
}

resource "aws_key_pair" "key" {
  key_name   = "id_rsa"
  public_key = data.local_file.public_key.content
}

resource "aws_subnet" "spot_private_subnet" {
  # creates a subnet
  cidr_block        = cidrsubnet(data.terraform_remote_state.env_setup.outputs.vpc_cidr_block, 8, 1)
  vpc_id            = data.terraform_remote_state.env_setup.outputs.vpc_id
  availability_zone = var.availability_zone
  tags = {
    Name = "spotkube"
  }
}

# Create eip for nat gateway
resource "aws_eip" "nat_eip" {
  vpc = true
}

# Create nat gateway
resource "aws_nat_gateway" "spotkube_nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = data.terraform_remote_state.env_setup.outputs.public_subnet_id

  tags = {
    Name = "spotkube_nat"
  }
}

# Create a route table for nat gateway
resource "aws_route_table" "public_rt_nat" {
  vpc_id = data.terraform_remote_state.env_setup.outputs.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.spotkube_nat.id
  }
}

resource "aws_route_table_association" "public_rt_nat_a" {
  subnet_id = aws_subnet.spot_private_subnet.id
  route_table_id = aws_route_table.public_rt_nat.id
}

resource "aws_security_group" "ingress_kubeapi" {
  name_prefix = "allow-kubeapi-sg"
  vpc_id = data.terraform_remote_state.env_setup.outputs.vpc_id

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Kube api Ingress"
  }
}

resource "aws_security_group" "ingress_prometheus" {
  name_prefix = "allow-prom-sg"
  vpc_id = data.terraform_remote_state.env_setup.outputs.vpc_id

  ingress {
    from_port   = 30000
    to_port     = 30000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 32000
    to_port     = 32000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Prometheus Ingress"
  }
}
