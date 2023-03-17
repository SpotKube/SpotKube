output "subnet_id" {
  value = aws_subnet.spot_subnet.id
}

output "security_group_id" {
  value = aws_security_group.ingress_ssh.id
}
