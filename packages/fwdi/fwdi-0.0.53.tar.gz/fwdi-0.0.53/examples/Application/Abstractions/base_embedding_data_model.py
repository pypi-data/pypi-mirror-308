from abc import ABCMeta, abstractmethod

from fwdi.Application.Abstractions import BaseServiceFWDI

from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Application.DTO.Request.rag_question_project import RagQuestionProject
from Application.DTO.Response.responce_emb_sentences_model import EmbedddingSentencesModelView
from Presentation.ViewModels.EmbeddingViewModel import EmbeddingViewModel


class BaseEmbeddingDataModel(BaseServiceFWDI, metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def embedding_model_v3(infer: BaseEmbeddingModel,
                           lst_models: EmbeddingViewModel) -> EmbedddingSentencesModelView:
        pass

    @staticmethod
    @abstractmethod
    def embedding_question(infer: BaseEmbeddingModel,
                           question: RagQuestionProject) -> EmbedddingSentencesModelView:
        pass


