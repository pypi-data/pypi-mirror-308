from pydantic import BaseModel

class RagQuestionProject(BaseModel):
        question: str
        project: str
        k_top: int
        max_new_token: int