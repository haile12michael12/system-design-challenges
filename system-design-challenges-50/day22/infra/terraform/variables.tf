variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr_1" {
  description = "CIDR block for public subnet 1"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_cidr_2" {
  description = "CIDR block for public subnet 2"
  type        = string
  default     = "10.0.2.0/24"
}

variable "private_subnet_cidr_1" {
  description = "CIDR block for private subnet 1"
  type        = string
  default     = "10.0.11.0/24"
}

variable "private_subnet_cidr_2" {
  description = "CIDR block for private subnet 2"
  type        = string
  default     = "10.0.12.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "db_instance_class" {
  description = "Database instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "feed_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "feed_user"
}

variable "cache_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.medium"
}

variable "mq_instance_type" {
  description = "MQ instance type"
  type        = string
  default     = "kafka.t3.small"
}