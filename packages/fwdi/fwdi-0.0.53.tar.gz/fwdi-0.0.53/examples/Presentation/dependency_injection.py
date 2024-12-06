from fwdi.WebApp.web_application import WebApplication
from Presentation.Endpoints.embedding_endpoints import EmbeddingEndpoints



class DependencyInjection:
    from fwdi.WebApp.web_application_builder import WebApplicationBuilder

    def AddEndpoints(app: WebApplication):
        app.map_post(f'/api/v1.0/embedding_models', EmbeddingEndpoints.embedding_models)
        app.map_post(f'/api/v1.0/embedding_question', EmbeddingEndpoints.embedding_question)

    def AddScope(builder: WebApplicationBuilder):
        scopes = {
            "admin": "Administration access.",
            "embedding": "Embedding access"
        }
        builder.add_scope(scopes)