output "fastapi_output" {
  description = "Fastapi ComponentAsset outputs consumed by other components."
  value = {
    namespace        = var.model_router_output.namespace
    deployment_name  = kubernetes_deployment_v1.fastapi_app.metadata[0].name
    service_name     = kubernetes_service_v1.fastapi_service.metadata[0].name
    service_ip       = kubernetes_service_v1.fastapi_service.spec[0].cluster_ip
    service_port     = kubernetes_service_v1.fastapi_service.spec[0].port[0].port
    service_endpoint = "${kubernetes_service_v1.fastapi_service.metadata[0].name}.${var.model_router_output.namespace}.svc.cluster.local"
    secret_name      = kubernetes_secret_v1.fastapi_envs.metadata[0].name
    replica_count    = kubernetes_deployment_v1.fastapi_app.spec[0].replicas
    image_used       = var.image
    framework_used   = var.framework
    llm_dns          = var.model_router_output.server_service_dns
    llm_port         = var.model_router_output.server_service_port
    redis_host       = var.redis_host
    redis_port       = var.redis_port
  }
}

output "mpp_report" {
  description = "Comprehensive output map for component consumption by other modules"
  value = {
    namespace        = var.model_router_output.namespace
    deployment_name  = kubernetes_deployment_v1.fastapi_app.metadata[0].name
    service_name     = kubernetes_service_v1.fastapi_service.metadata[0].name
    service_ip       = kubernetes_service_v1.fastapi_service.spec[0].cluster_ip
    service_port     = kubernetes_service_v1.fastapi_service.spec[0].port[0].port
    service_endpoint = "${kubernetes_service_v1.fastapi_service.metadata[0].name}.${var.model_router_output.namespace}.svc.cluster.local"
    secret_name      = kubernetes_secret_v1.fastapi_envs.metadata[0].name
    replica_count    = kubernetes_deployment_v1.fastapi_app.spec[0].replicas
    image_used       = var.image
    framework_used   = var.framework
    llm_dns          = var.model_router_output.server_service_dns
    llm_port         = var.model_router_output.server_service_port
    redis_host       = var.redis_host
    redis_port       = var.redis_port
  }
}
