# Create namespace for agent-runtime
resource "kubernetes_namespace_v1" "namespace" {
  metadata {
    name = var.namespace
  }
}

# Create secret for agent-runtime environment variables
resource "kubernetes_secret_v1" "agent_runtime_envs" {
  metadata {
    name      = "agent-runtime-secrets"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
  }

  type = "Opaque"

  data = {
    MODEL_ROUTER_URL = var.model_router_url
    REDIS_HOST       = var.redis_host
    REDIS_PORT       = tostring(var.redis_port)
    REDIS_PASSWORD   = var.redis_password
    FRAMEWORK        = var.framework
  }

  depends_on = [kubernetes_namespace_v1.namespace]
}

# Create deployment for agent-runtime application
resource "kubernetes_deployment_v1" "agent_runtime_app" {
  metadata {
    name      = "agent-runtime-app"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
    labels = {
      app = "agent-runtime"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "agent-runtime"
      }
    }

    template {
      metadata {
        labels = {
          app = "agent-runtime"
        }
      }

      spec {
        container {
          name  = "agent-runtime"
          image = var.image
          
          port {
            container_port = var.pod_port
            name           = "http"
          }
          
          # Load all environment variables from secret
          env_from {
            secret_ref {
              name = kubernetes_secret_v1.agent_runtime_envs.metadata[0].name
            }
          }
          
          # Resource requests and limits
          resources {
            requests = {
              cpu    = "100m"
              memory = "256Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }
          
          # Liveness probe
          liveness_probe {
            http_get {
              path = "/health"
              port = var.pod_port
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }
          
          # Readiness probe
          readiness_probe {
            http_get {
              path = "/ready"
              port = var.pod_port
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }

  depends_on = [kubernetes_secret_v1.agent_runtime_envs]
}

# Create service for agent-runtime
resource "kubernetes_service_v1" "agent_runtime_service" {
  metadata {
    name      = "agent-runtime-service"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
    labels = {
      app = "agent-runtime"
    }
  }

  spec {
    selector = {
      app = "agent-runtime"
    }

    port {
      port        = var.server_port
      target_port = var.pod_port
      protocol    = "TCP"
      name        = "http"
    }

    type = "ClusterIP"
  }

  depends_on = [kubernetes_deployment_v1.agent_runtime_app]
}
