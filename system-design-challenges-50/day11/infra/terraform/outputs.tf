output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.autoscaler_alb.dns_name
}

output "backend_service_url" {
  description = "URL of the backend service"
  value       = "http://${aws_lb.autoscaler_alb.dns_name}:8000"
}

output "frontend_service_url" {
  description = "URL of the frontend service"
  value       = "http://${aws_lb.autoscaler_alb.dns_name}:3000"
}

output "db_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.autoscaler_db.endpoint
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_cluster.autoscaler_redis.cache_nodes[0].address
}