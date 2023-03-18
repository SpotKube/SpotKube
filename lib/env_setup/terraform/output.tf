output "subnet_id" {
  value = aws_subnet.spot_subnet.id
}

output "security_group_id" {
  value = aws_security_group.ingress_ssh.id
}

# Save the public ip of the management node
output "management_node_public_ip" {
  value = "${aws_instance.management_node.public_ip}"
}
