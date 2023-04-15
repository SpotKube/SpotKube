variable "availability_zone" {
  default = "us-east-1a"
}

variable "ami_id" {
  default = "ami-0557a15b87f6559cf"
}

variable "pub_id_file_path" {
  # default = "/home/ksr/.ssh/id_spotkube.pub"
  type        = string
  description = "This contains the public key file path"
}

variable "aws_shared_config_file_path" {
  # default = "/home/pasindu/.aws/config"
  type        = string
  description = "This contains the aws config file path"
}

variable "aws_shared_credentials_file_path" {
  # default = "/home/pasindu/.aws/credentials"
  type        = string
  description = "This contains the aws credentials file path"
}



