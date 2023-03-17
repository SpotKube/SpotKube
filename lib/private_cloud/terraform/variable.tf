# Variables
variable "keypair" {
  type    = string
  default = "admin"   # name of keypair created 
}

variable "network" {
  type    = string
  default = "private" # default network to be used
}

variable "security_groups" {
  type    = list(string)
  default = ["default"]  # Name of default security group
}