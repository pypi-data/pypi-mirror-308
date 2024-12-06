from abc import ABCMeta, abstractmethod

from fwdi.Application.Abstractions import BaseServiceFWDI


class BaseEmbeddingModel(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def encode(self, sentences: list) -> list:
        pass