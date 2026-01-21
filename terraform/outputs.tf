output "model_router_output" {
  description = "This is the model_router_output ComponentAsset consumed by other components."
  value = {
    namespace           = kubernetes_namespace_v1.namespace.metadata[0].name
    image_used          = var.image
    replica_count       = kubernetes_deployment_v1.server_app.spec[0].replicas
    deployment_name     = kubernetes_deployment_v1.server_app.metadata[0].name
    server_service_ip   = kubernetes_service_v1.server_service.spec[0].cluster_ip
    server_service_port = kubernetes_service_v1.server_service.spec[0].port[0].port
    server_service_dns  = "${kubernetes_service_v1.server_service.metadata[0].name}.${kubernetes_service_v1.server_service.metadata[0].namespace}.svc.cluster.local"
  }
}

output "mpp_report" {
  description = "This is the string key-value map containing properties presented to the user for consuming this component."
  value = {
    "namespace"           = kubernetes_namespace_v1.namespace.metadata[0].name
    "image_used"          = var.image
    "replica_count"       = kubernetes_deployment_v1.server_app.spec[0].replicas
    "deployment_name"     = kubernetes_deployment_v1.server_app.metadata[0].name
    "server_service_ip"   = kubernetes_service_v1.server_service.spec[0].cluster_ip
    "server_service_port" = kubernetes_service_v1.server_service.spec[0].port[0].port
    "server_service_dns"  = "${kubernetes_service_v1.server_service.metadata[0].name}.${kubernetes_service_v1.server_service.metadata[0].namespace}.svc.cluster.local"
  }
}