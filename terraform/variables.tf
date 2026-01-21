variable "image" {
  description = "Docker image to use for the application"
  type        = string
  default     = "310378384655.dkr.ecr.us-east-1.amazonaws.com/agent-runtime:v1"
}

variable "replicas" {
  description = "Number of replicas"
  type        = number
  default     = 1
}

variable "pod_port" {
  description = "server port inside the pod"
  type        = number
  default     = 8000
}

variable "server_port" {
  description = "kubernetes service port"
  type        = number
  default     = 8000
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "agent-runtime"
}

# Agent Runtime Environment Variables
variable "model_router_url" {
  description = "URL for the Model Router service"
  type        = string
  default     = "http://model-router-server-service.model-router.svc.cluster.local:8000"
  sensitive   = false
}

variable "redis_host" {
  description = "Redis host address"
  type        = string
  sensitive   = false
}

variable "redis_port" {
  description = "Redis port"
  type        = number
  default     = 6379
  sensitive   = false
}

variable "redis_password" {
  description = "Redis password"
  type        = string
  sensitive   = true
}

variable "framework" {
  description = "AI framework to use (langgraph or crewai)"
  type        = string
  default     = "langgraph"
  sensitive   = false
}