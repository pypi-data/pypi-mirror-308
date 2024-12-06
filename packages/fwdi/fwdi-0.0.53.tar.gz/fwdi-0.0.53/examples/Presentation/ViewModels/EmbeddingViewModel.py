from pydantic import BaseModel

class EmbeddingViewModel(BaseModel):
    datetime: str
    models: list[str]
