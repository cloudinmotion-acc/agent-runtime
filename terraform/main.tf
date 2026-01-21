resource "kubernetes_secret_v1" "fastapi_envs" {
  metadata {
    name      = "fastapi-secrets"
    namespace = var.model_router_output.namespace
  }

  type = "Opaque"

  data = {
    MODEL_ROUTER_URL = var.model_router_output.server_service_dns != "" ? "http://${var.model_router_output.server_service_dns}:${tostring(var.model_router_output.server_service_port)}" : "http://model-router-server-service.model-router.svc.cluster.local:8000"
    REDIS_HOST       = var.redis_host
    REDIS_PORT       = tostring(var.redis_port)
    REDIS_PASSWORD   = var.redis_password
    FRAMEWORK        = var.framework
  }
}

resource "kubernetes_deployment_v1" "fastapi_app" {
  metadata {
    name      = "fastapi-app"
    namespace = var.model_router_output.namespace
    labels = {
      app = "fastapi"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "fastapi"
      }
    }

    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }

      spec {
        container {
          name  = "fastapi"
          image = var.image
          
          port {
            container_port = var.pod_port
            name           = "http"
          }
          
          # Load all environment variables from secret
          env_from {
            secret_ref {
              name = kubernetes_secret_v1.fastapi_envs.metadata[0].name
            }
          }
          
          # Resource requests and limits
          resources {
            requests = {
              cpu    = var.resource_requests.cpu
              memory = var.resource_requests.memory
            }
            limits = {
              cpu    = var.resource_limits.cpu
              memory = var.resource_limits.memory
            }
          }
        }
      }
    }
  }

  depends_on = [kubernetes_secret_v1.fastapi_envs]
}

# Create service for fastapi
resource "kubernetes_service_v1" "fastapi_service" {
  metadata {
    name      = "fastapi-service"
    namespace = var.model_router_output.namespace
    labels = {
      app = "fastapi"
    }
  }

  spec {
    selector = {
      app = "fastapi"
    }

    port {
      port        = var.server_port
      target_port = var.pod_port
      protocol    = "TCP"
      name        = "http"
    }

    type = var.service_type
  }

  depends_on = [kubernetes_deployment_v1.fastapi_app]
}
