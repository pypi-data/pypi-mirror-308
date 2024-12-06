from fwdi.Application.Abstractions import BaseServiceCollectionFWDI
from fwdi.Application.Configs.service_congif import ServiceConfig

from Application.Abstractions.base_embedding_data_model import BaseEmbeddingDataModel
from Application.Usecase.embedding_data_model import EmbeddingDataModel


class DependencyInjection():

    @staticmethod
    def AddApplication(services:BaseServiceCollectionFWDI):
        services.AddSingleton(BaseEmbeddingDataModel, EmbeddingDataModel)

    @staticmethod
    def AddConfig(services:BaseServiceCollectionFWDI):
        ServiceConfig.service_avaible = True
        ServiceConfig.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        ServiceConfig.ALGORITHM = "HS256"
        ServiceConfig.ACCESS_TOKEN_EXPIRE_MINUTES = 10000

        services.AddSingleton(ServiceConfig)
