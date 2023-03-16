output "spot_instances" {
  value = [ for instance in aws_spot_instance_request.worker_nodes: {
    id = instance.id
    public_ip = instance.public_ip
    private_ip = instance.private_ip
    instance_type = instance.instance_type
    key_name = instance.key_name
    subnet_id = instance.subnet_id
    vpc_security_group_ids = instance.vpc_security_group_ids
    associate_public_ip_address = instance.associate_public_ip_address
    user_data = instance.user_data
    tags = instance.tags
  }]
}
