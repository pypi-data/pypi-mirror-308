from fwdi.Application.Abstractions import BaseServiceCollectionFWDI

from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Infrastructure.Embeddings.embedding_models import EmbeddingModel



class DependencyInjection():

    @staticmethod
    def AddInfrastructure(services:BaseServiceCollectionFWDI):
        services.AddSingleton(BaseEmbeddingModel, EmbeddingModel)