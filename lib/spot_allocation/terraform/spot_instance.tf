module "env" {
  source = "../../env_setup/terraform"
}

resource "aws_spot_instance_request" "worker_nodes" {
  for_each = var.spot_instances
  ami                    = "${var.ami_id}"
  spot_price             = "${each.value.spot_price}"
  instance_type          = "${each.value.instance_type}"
  spot_type              = "one-time"
  block_duration_minutes = "120"
  wait_for_fulfillment   = "true"
  key_name               = "spot_key"

  security_groups = ["${module.env.aws_subnet.spot_subnet.id}"]
  # subnet_id = "${aws_subnet.subnet-uno.id}"
}
