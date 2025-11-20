variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "autoscaler"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  type        = string
  default     = "password"
}

variable "redis_node_type" {
  description = "Redis node type"
  type        = string
  default     = "cache.t3.micro"
}