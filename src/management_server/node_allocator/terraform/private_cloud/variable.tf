# Variables
variable "keypair" {
  type    = string
  default = "admin"   # name of keypair created 
}

variable "private_instances" {
  type = map(any)
}
