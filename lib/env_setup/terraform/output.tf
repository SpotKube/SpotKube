output "subnet_id" {
  value = aws_subnet.spot_public_subnet.id
}

output "security_group_ssh_id" {
  value = aws_security_group.ingress_ssh.id
}

output "security_group_http_id" {
  value = aws_security_group.ingress_http.id
}

output "security_group_https_id" {
  value = aws_security_group.ingress_https.id
}

# Save the public ip of the management node
output "management_node_public_ip" {
  value = aws_instance.management_node.public_ip
}
