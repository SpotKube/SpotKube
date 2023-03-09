data "terraform_remote_state" "env_setup" {
  backend = "s3"

  config = {
    bucket = "spotkube-terraform-state-bucket"
    key    = "env_setup-terraform.tfstate"
    region = "us-west-2"
   }
}

resource "aws_spot_instance_request" "worker_nodes" {
  for_each = var.spot_instances
  ami                    = "${var.ami_id}"
  spot_price             = "${each.value.spot_price}"
  instance_type          = "${each.value.instance_type}"
  spot_type              = "one-time"
  wait_for_fulfillment   = "true"
  key_name               = "spotkube_key" # Need to change

  security_groups = ["${data.terraform_remote_state.env_setup.outputs.security_group_id}"]
  subnet_id = "${data.terraform_remote_state.env_setup.outputs.subnet_id}"

  tags = {
    "Name" : "${each.key}"
  }
}
