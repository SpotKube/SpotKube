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
  key_name   = "spotkube_management_key"
  public_key = data.local_file.public_key.content
}
