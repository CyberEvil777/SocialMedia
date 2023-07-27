from pydantic import BaseModel


class Response(BaseModel):
    """Схема для ответа"""

    message: str
