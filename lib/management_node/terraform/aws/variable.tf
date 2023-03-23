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

variable "pub_id_file_path" {
  default = "/home/ubuntu/.ssh/id_rsa.pub"
  type        = string
  description = "This contains the public key file path"
}
