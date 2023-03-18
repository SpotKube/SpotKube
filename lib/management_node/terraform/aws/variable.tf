variable "instance_type" {
  type = string
  default = "t2.micro"
}

variable "ami_id" {
  default = "ami-0557a15b87f6559cf"
}

variable "spot_instances" {
  type = map
}
