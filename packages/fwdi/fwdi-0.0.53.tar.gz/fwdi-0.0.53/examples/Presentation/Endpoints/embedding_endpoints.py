from fastapi import Security, Depends
from fwdi.Application.Abstractions import BaseServiceFWDI
from fwdi.Application.DTO.Auth import User
from fwdi.Infrastructure.JwtService import JwtServiceFWDI

from Application.DTO.Request.rag_question_project import RagQuestionProject
from Application.DTO.Response.responce_emb_sentences_model import EmbedddingSentencesModelView
from Application.Usecase.embedding_data_model import EmbeddingDataModel
from Presentation.ViewModels.EmbeddingViewModel import EmbeddingViewModel
from Utilites.ext_rest import RestResponse


class EmbeddingEndpoints(BaseServiceFWDI):
    count = 0
    @staticmethod
    def embedding_models(embedding_view_model: EmbedddingSentencesModelView, embedding_model: EmbeddingDataModel=Depends(),
             current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["embedding"]),):
        try:
            embedding_model = embedding_model.embedding_model_v3(embedding_view_model)

            return RestResponse.response_200(embedding_model)
        except Exception as ex:
            EmbeddingEndpoints.__log__(ex, 'error')

        finally:
            del embedding_model
            EmbeddingEndpoints.__log__(f"ITTERATION:{EmbeddingEndpoints.count }")
            EmbeddingEndpoints.count += 1

    @staticmethod
    def embedding_question(question_pack:RagQuestionProject,
                           embedding_model: EmbeddingDataModel=Depends(),
                            current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["embedding"]),):

        try:
            embedding_question = EmbeddingDataModel.embedding_question(question_pack)
            del question_pack

            return RestResponse.response_200(embedding_question)
        except Exception as ex:
            EmbeddingEndpoints.__log__(ex, 'error')

        finally:
            del embedding_question
            EmbeddingEndpoints.__log__(f"ITTERATION:{EmbeddingEndpoints.count}")
            EmbeddingEndpoints.count += 1
