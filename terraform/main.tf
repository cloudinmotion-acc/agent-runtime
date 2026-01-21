resource "kubernetes_secret_v1" "llm_envs" {
  metadata {
    name      = "model-router-llm-secrets"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
  }

  data = {
    OPENAI_API_KEY = var.openai_api_key
  }

  type = "Opaque"
}


resource "kubernetes_deployment_v1" "server_app" {
  metadata {
    name      = "model-router-server-app"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
    labels = {
      app = "server"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "server"
      }
    }

    template {
      metadata {
        labels = {
          app = "server"
        }
      }

      spec {
        container {
          name  = "model-router-server"
          image = var.image
          port {
            container_port = var.pod_port
          }
          env_from {
            secret_ref {
              name = kubernetes_secret_v1.llm_envs.metadata[0].name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "server_service" {
  metadata {
    name      = "model-router-server-service"
    namespace = kubernetes_namespace_v1.namespace.metadata[0].name
  }

  spec {
    selector = {
      app = "server"
    }

    port {
      port        = var.server_port
      target_port = var.pod_port
    }

    type = "ClusterIP"
  }
}
