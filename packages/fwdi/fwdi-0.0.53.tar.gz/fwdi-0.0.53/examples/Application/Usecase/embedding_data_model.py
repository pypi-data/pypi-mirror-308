from Application.Abstractions.base_embedding_data_model import BaseEmbeddingDataModel
from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Application.DTO.Request.rag_question_project import RagQuestionProject
from Application.DTO.Response.responce_emb_sentences_model import EmbedddingSentencesModelView
from Presentation.ViewModels.EmbeddingViewModel import EmbeddingViewModel


class EmbeddingDataModel(BaseEmbeddingDataModel):

    @staticmethod
    def embedding_model_v3(lst_models: EmbedddingSentencesModelView,
                           infer: BaseEmbeddingModel) -> EmbedddingSentencesModelView:
        if not lst_models == None:
            try:
                only_text = [item["text"] for item in lst_models.embedding_sentences]
                embedding = infer.encode(only_text)
                if not embedding is None:
                    response_model = EmbedddingSentencesModelView(embedding_sentences=embedding)

                del only_text
                del embedding
                return response_model
            except Exception as ex:
                EmbeddingDataModel.__log__(f"ERROR:{ex}")

        return None

    @staticmethod
    def embedding_question(question: RagQuestionProject,
                           infer: BaseEmbeddingModel) -> EmbedddingSentencesModelView:
        if not question == None:
            try:
                embedding = infer.encode([question.question])
                if not embedding is None:
                    response_model = EmbedddingSentencesModelView(embedding_sentences=embedding)
                del embedding
                return response_model
            except Exception as ex:
                EmbeddingDataModel.__log__(f"ERROR:{ex}")

        return None