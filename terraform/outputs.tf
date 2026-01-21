output "agent_runtime_output" {
  description = "Agent Runtime ComponentAsset outputs consumed by other components."
  value = {
    namespace           = kubernetes_namespace_v1.namespace.metadata[0].name
    image_used          = var.image
    replica_count       = kubernetes_deployment_v1.agent_runtime_app.spec[0].replicas
    deployment_name     = kubernetes_deployment_v1.agent_runtime_app.metadata[0].name
    service_ip          = kubernetes_service_v1.agent_runtime_service.spec[0].cluster_ip
    service_port        = kubernetes_service_v1.agent_runtime_service.spec[0].port[0].port
    service_dns         = "${kubernetes_service_v1.agent_runtime_service.metadata[0].name}.${kubernetes_service_v1.agent_runtime_service.metadata[0].namespace}.svc.cluster.local"
    secret_name         = kubernetes_secret_v1.agent_runtime_envs.metadata[0].name
    framework           = var.framework
  }
}

output "mpp_report" {
  description = "String key-value map containing properties presented to the user for consuming this component."
  value = {
    "namespace"           = kubernetes_namespace_v1.namespace.metadata[0].name
    "image_used"          = var.image
    "replica_count"       = kubernetes_deployment_v1.agent_runtime_app.spec[0].replicas
    "deployment_name"     = kubernetes_deployment_v1.agent_runtime_app.metadata[0].name
    "service_ip"          = kubernetes_service_v1.agent_runtime_service.spec[0].cluster_ip
    "service_port"        = kubernetes_service_v1.agent_runtime_service.spec[0].port[0].port
    "service_dns"         = "${kubernetes_service_v1.agent_runtime_service.metadata[0].name}.${kubernetes_service_v1.agent_runtime_service.metadata[0].namespace}.svc.cluster.local"
    "secret_name"         = kubernetes_secret_v1.agent_runtime_envs.metadata[0].name
    "framework"           = var.framework
    "model_router_url"    = var.model_router_url
    "redis_host"          = var.redis_host
  }
}

output "kubernetes_secret_name" {
  description = "Name of the Kubernetes secret containing agent runtime configuration"
  value       = kubernetes_secret_v1.agent_runtime_envs.metadata[0].name
}

output "service_endpoint" {
  description = "Service endpoint DNS name for agent runtime"
  value       = "${kubernetes_service_v1.agent_runtime_service.metadata[0].name}.${kubernetes_service_v1.agent_runtime_service.metadata[0].namespace}.svc.cluster.local:${kubernetes_service_v1.agent_runtime_service.spec[0].port[0].port}"
}