data "terraform_remote_state" "env_setup" {
  backend = "s3"

  config = {
    bucket = "spotkube-terraform-state-bucket"
    key    = "env_setup-terraform.tfstate"
    region = "us-west-2"
   }
}

data "local_file" "public_key" {
  filename = "${var.pub_id_file_path}"
}

resource "aws_key_pair" "key" {
  key_name   = "spotkube_management_key"
  public_key = "${data.local_file.public_key.content}"
}

resource "aws_spot_instance_request" "worker_nodes" {
  for_each = var.spot_instances
  ami                    = "${var.ami_id}"
  spot_price             = "${each.value.spot_price}"
  instance_type          = "${each.value.instance_type}"
  spot_type              = "one-time"
  wait_for_fulfillment   = "true"
  key_name               = "${aws_key_pair.key.key_name}"

  security_groups = ["${data.terraform_remote_state.env_setup.outputs.security_group_id}"]
  subnet_id = "${data.terraform_remote_state.env_setup.outputs.subnet_id}"

  tags = {
    "Name" : "${each.key}"
  }
}
