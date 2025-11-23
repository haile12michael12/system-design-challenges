output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.feed_vpc.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

output "api_security_group_id" {
  description = "ID of the API security group"
  value       = aws_security_group.api_sg.id
}

output "db_security_group_id" {
  description = "ID of the database security group"
  value       = aws_security_group.db_sg.id
}

output "cache_security_group_id" {
  description = "ID of the cache security group"
  value       = aws_security_group.cache_sg.id
}

output "mq_security_group_id" {
  description = "ID of the message queue security group"
  value       = aws_security_group.mq_sg.id
}