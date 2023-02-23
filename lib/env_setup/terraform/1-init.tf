resource "aws_vpc" "spot-vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "spot-subnet" {
  # creates a subnet
  cidr_block        = "${cidrsubnet(aws_vpc.test-env.cidr_block, 3, 1)}"
  vpc_id            = "${aws_vpc.spot-vpc.id}"
  availability_zone = var.availability_zone
}

# resource "aws_internet_gateway" "spot-igw" {
#   vpc_id = "${aws_vpc.spot-vpc.id}"
# }

