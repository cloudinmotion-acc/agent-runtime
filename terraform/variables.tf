variable "model_router_output" {
  description = "model_router_output for fastapi deployment"
  type = object({
    namespace              = string
    server_service_dns     = string
    server_service_port    = number
  })
}

variable "image" {
  description = "Docker image URI from ECR for the fastapi application"
  type        = string
  nullable    = false
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 2
  validation {
    condition     = var.replicas > 0
    error_message = "Replicas must be greater than 0"
  }
}

variable "pod_port" {
  description = "Port exposed by the container inside the pod"
  type        = number
  default     = 9000
  validation {
    condition     = var.pod_port >= 1 && var.pod_port <= 65535
    error_message = "Pod port must be between 1 and 65535"
  }
}

variable "server_port" {
  description = "Kubernetes service port"
  type        = number
  default     = 9000
  validation {
    condition     = var.server_port >= 1 && var.server_port <= 65535
    error_message = "Server port must be between 1 and 65535"
  }
}

variable "service_type" {
  description = "Kubernetes service type (ClusterIP, NodePort, LoadBalancer)"
  type        = string
  default     = "ClusterIP"
  validation {
    condition     = contains(["ClusterIP", "NodePort", "LoadBalancer"], var.service_type)
    error_message = "Service type must be one of: ClusterIP, NodePort, LoadBalancer"
  }
}

# variable "model_router_url" {
#   description = "URL for the Model Router service"
#   type        = string
#   default     = "http://model-router-server-service.model-router.svc.cluster.local:8000"
#   sensitive   = false
# }

variable "redis_host" {
  description = "Redis host address"
  type        = string
  sensitive   = false
  nullable    = false
}

variable "redis_port" {
  description = "Redis port number"
  type        = number
  default     = 6379
  sensitive   = false
  validation {
    condition     = var.redis_port >= 1 && var.redis_port <= 65535
    error_message = "Redis port must be between 1 and 65535"
  }
}

variable "redis_password" {
  description = "Redis password for authentication"
  type        = string
  sensitive   = true
  nullable    = false
}

variable "framework" {
  description = "AI framework to use for fastapi (langgraph or crewai)"
  type        = string
  default     = "langgraph"
  validation {
    condition     = contains(["langgraph", "crewai"], var.framework)
    error_message = "Framework must be one of: langgraph, crewai"
  }
  sensitive = false
}

variable "resource_requests" {
  description = "Resource requests for the container (cpu, memory)"
  type = object({
    cpu    = string
    memory = string
  })
  default = {
    cpu    = "100m"
    memory = "256Mi"
  }
}

variable "resource_limits" {
  description = "Resource limits for the container (cpu, memory)"
  type = object({
    cpu    = string
    memory = string
  })
  default = {
    cpu    = "500m"
    memory = "512Mi"
  }
}
